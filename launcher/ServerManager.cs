using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ARTHA.Launcher;

public class ServerManager
{
    private Process? _backendProcess;
    private Process? _frontendProcess;
    private readonly HttpClient _httpClient = new() { Timeout = TimeSpan.FromSeconds(2) };
    private System.Threading.Timer? _healthTimer;
    private readonly object _lock = new();

    public string RootDir { get; private set; }
    public string NodeExecutable { get; private set; } = "node";
    public int BackendPort { get; private set; } = 11001;
    public int FrontendPort { get; private set; } = 11002;

    public bool IsBackendRunning => _backendProcess != null && !_backendProcess.HasExited;
    public bool IsFrontendRunning => _frontendProcess != null && !_frontendProcess.HasExited;

    public bool IsBackendHealthy { get; private set; }
    public bool IsFrontendHealthy { get; private set; }

    public event Action<LogItem>? LogReceived;
    public event Action? StatusChanged;

    public ServerManager()
    {
        RootDir = LocateProjectRoot();
        ResolveNodePath();
        ResolvePorts();
    }

    private string LocateProjectRoot()
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        while (!string.IsNullOrEmpty(dir))
        {
            if (File.Exists(Path.Combine(dir, "server.js")) && File.Exists(Path.Combine(dir, "package.json")))
            {
                return dir;
            }
            DirectoryInfo? parent = Directory.GetParent(dir);
            if (parent == null) break;
            dir = parent.FullName;
        }
        return AppDomain.CurrentDomain.BaseDirectory;
    }

    private void ResolveNodePath()
    {
        string bundledNode = Path.Combine(RootDir, "node", "node.exe");
        if (File.Exists(bundledNode))
        {
            NodeExecutable = bundledNode;
            return;
        }

        // Try PATH
        try
        {
            using var proc = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "where.exe",
                    Arguments = "node",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }
            };
            proc.Start();
            string output = proc.StandardOutput.ReadToEnd();
            proc.WaitForExit();
            var lines = output.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            if (lines.Length > 0 && File.Exists(lines[0].Trim()))
            {
                NodeExecutable = lines[0].Trim();
                return;
            }
        }
        catch
        {
            // fallback
        }

        NodeExecutable = "node";
    }

    public void ResolvePorts()
    {
        try
        {
            string portFile = Path.Combine(RootDir, "data", "port.txt");
            if (File.Exists(portFile))
            {
                string text = File.ReadAllText(portFile).Trim();
                if (int.TryParse(text, out int p) && p >= 1024 && p <= 65535)
                {
                    BackendPort = p;
                }
            }
        }
        catch { }

        FrontendPort = 11002;
    }

    public async Task StartAsync()
    {
        lock (_lock)
        {
            if (IsBackendRunning || IsFrontendRunning)
            {
                AddLog(LogSource.System, "Servers are already running or starting.");
                return;
            }
        }

        AddLog(LogSource.System, $"==================================================");
        AddLog(LogSource.System, $"  Starting ARTHA Services");
        AddLog(LogSource.System, $"  Root Directory: {RootDir}");
        AddLog(LogSource.System, $"  Node Runtime:   {NodeExecutable}");
        AddLog(LogSource.System, $"==================================================");

        // Pre-step: Bundle tesseract assets if script exists
        string tesseractScript = Path.Combine(RootDir, "scripts", "bundle-tesseract-assets.mjs");
        if (File.Exists(tesseractScript))
        {
            AddLog(LogSource.System, "Checking Tesseract OCR assets...");
            try
            {
                using var p = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = NodeExecutable,
                        Arguments = $"\"{tesseractScript}\"",
                        WorkingDirectory = RootDir,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    }
                };
                p.Start();
                await p.WaitForExitAsync();
            }
            catch (Exception ex)
            {
                AddLog(LogSource.Error, $"Tesseract asset preparation notice: {ex.Message}");
            }
        }

        // Start Backend
        StartBackend();

        // Start Frontend
        StartFrontend();

        // Start health monitor timer
        _healthTimer?.Dispose();
        _healthTimer = new System.Threading.Timer(CheckHealthCallback, null, 1500, 3000);

        StatusChanged?.Invoke();
    }

    private void StartBackend()
    {
        string serverJs = Path.Combine(RootDir, "server.js");
        if (!File.Exists(serverJs))
        {
            AddLog(LogSource.Error, $"Cannot find server.js at: {serverJs}");
            return;
        }

        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = NodeExecutable,
                Arguments = "server.js",
                WorkingDirectory = RootDir,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };

            _backendProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
            _backendProcess.OutputDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    AddLog(LogSource.Backend, e.Data);
                }
            };
            _backendProcess.ErrorDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    AddLog(LogSource.Error, $"[Backend Err] {e.Data}");
                }
            };
            _backendProcess.Exited += (s, e) =>
            {
                IsBackendHealthy = false;
                AddLog(LogSource.System, "Backend process has stopped.");
                StatusChanged?.Invoke();
            };

            _backendProcess.Start();
            JobManager.AttachProcess(_backendProcess);
            _backendProcess.BeginOutputReadLine();
            _backendProcess.BeginErrorReadLine();

            AddLog(LogSource.System, $"Backend process started (PID: {_backendProcess.Id}). Listening on port {BackendPort}...");
        }
        catch (Exception ex)
        {
            AddLog(LogSource.Error, $"Failed to launch Backend: {ex.Message}");
        }
    }

    private void StartFrontend()
    {
        string viteJs = Path.Combine(RootDir, "node_modules", "vite", "bin", "vite.js");
        string viteCmd = Path.Combine(RootDir, "node_modules", ".bin", "vite.cmd");
        string distDir = Path.Combine(RootDir, "dist");

        string launchFile = NodeExecutable;
        string launchArgs = "";

        if (File.Exists(viteJs))
        {
            launchFile = NodeExecutable;
            launchArgs = $"\"{viteJs}\"";
        }
        else if (File.Exists(viteCmd))
        {
            launchFile = viteCmd;
            launchArgs = "";
        }
        else if (Directory.Exists(distDir))
        {
            AddLog(LogSource.System, "Using compiled production assets in dist/. Backend serves frontend directly.");
            IsFrontendHealthy = true;
            return;
        }
        else
        {
            AddLog(LogSource.Error, "Neither Vite dev server nor dist/ directory found. Run npm install or npm run build.");
            return;
        }

        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = launchFile,
                Arguments = launchArgs,
                WorkingDirectory = RootDir,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };

            _frontendProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
            _frontendProcess.OutputDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    AddLog(LogSource.Frontend, e.Data);
                }
            };
            _frontendProcess.ErrorDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    AddLog(LogSource.Error, $"[Frontend Err] {e.Data}");
                }
            };
            _frontendProcess.Exited += (s, e) =>
            {
                IsFrontendHealthy = false;
                AddLog(LogSource.System, "Frontend dev server process has stopped.");
                StatusChanged?.Invoke();
            };

            _frontendProcess.Start();
            JobManager.AttachProcess(_frontendProcess);
            _frontendProcess.BeginOutputReadLine();
            _frontendProcess.BeginErrorReadLine();

            AddLog(LogSource.System, $"Frontend dev server started (PID: {_frontendProcess.Id}). Target port: {FrontendPort}...");
        }
        catch (Exception ex)
        {
            AddLog(LogSource.Error, $"Failed to launch Frontend: {ex.Message}");
        }
    }

    public async Task StopAsync()
    {
        _healthTimer?.Change(Timeout.Infinite, Timeout.Infinite);

        AddLog(LogSource.System, "Stopping background services...");

        await Task.Run(() =>
        {
            KillProcessTree(_backendProcess);
            KillProcessTree(_frontendProcess);
            _backendProcess = null;
            _frontendProcess = null;
            IsBackendHealthy = false;
            IsFrontendHealthy = false;
        });

        AddLog(LogSource.System, "All ARTHA services stopped.");
        StatusChanged?.Invoke();
    }

    public async Task RestartAsync()
    {
        AddLog(LogSource.System, "Restarting ARTHA services...");
        await StopAsync();
        await Task.Delay(800);
        ResolvePorts();
        await StartAsync();
    }

    private void KillProcessTree(Process? proc)
    {
        if (proc == null) return;
        try
        {
            if (!proc.HasExited)
            {
                // Kill process tree on Windows
                using var killer = Process.Start(new ProcessStartInfo
                {
                    FileName = "taskkill.exe",
                    Arguments = $"/F /T /PID {proc.Id}",
                    CreateNoWindow = true,
                    UseShellExecute = false
                });
                killer?.WaitForExit(3000);
                if (!proc.HasExited)
                {
                    proc.Kill(entireProcessTree: true);
                }
            }
        }
        catch { }
        finally
        {
            try { proc.Dispose(); } catch { }
        }
    }

    private async void CheckHealthCallback(object? state)
    {
        ResolvePorts();
        bool bHealthy = false;
        bool fHealthy = false;

        if (IsBackendRunning)
        {
            try
            {
                var resp = await _httpClient.GetAsync($"http://localhost:{BackendPort}/api/health");
                bHealthy = resp.IsSuccessStatusCode;
            }
            catch
            {
                try
                {
                    var resp = await _httpClient.GetAsync($"http://127.0.0.1:{BackendPort}/api/health");
                    bHealthy = resp.IsSuccessStatusCode;
                }
                catch
                {
                    bHealthy = false;
                }
            }
        }

        if (IsFrontendRunning)
        {
            try
            {
                var resp = await _httpClient.GetAsync($"http://localhost:{FrontendPort}/");
                fHealthy = resp.IsSuccessStatusCode;
            }
            catch
            {
                try
                {
                    var resp = await _httpClient.GetAsync($"http://[::1]:{FrontendPort}/");
                    fHealthy = resp.IsSuccessStatusCode;
                }
                catch
                {
                    try
                    {
                        var resp = await _httpClient.GetAsync($"http://127.0.0.1:{FrontendPort}/");
                        fHealthy = resp.IsSuccessStatusCode;
                    }
                    catch
                    {
                        fHealthy = false;
                    }
                }
            }
        }
        else if (Directory.Exists(Path.Combine(RootDir, "dist")) && bHealthy)
        {
            fHealthy = true; // Served by backend in production
        }

        if (bHealthy != IsBackendHealthy || fHealthy != IsFrontendHealthy)
        {
            IsBackendHealthy = bHealthy;
            IsFrontendHealthy = fHealthy;
            StatusChanged?.Invoke();
        }
    }

    public void AddLog(LogSource source, string message)
    {
        var item = new LogItem(source, message);
        LogReceived?.Invoke(item);
    }
}

