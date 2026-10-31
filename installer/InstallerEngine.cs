using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Win32;

namespace ARTHA.Installer;

public record InstallerProgress(int Percentage, string Status);

public class InstallerEngine
{
    public string SourceDir { get; private set; }
    public string TargetDir { get; set; }
    public bool CreateDesktopShortcut { get; set; } = true;
    public bool CreateStartMenuShortcut { get; set; } = true;
    public bool LaunchAfterInstall { get; set; } = true;

    public InstallerEngine()
    {
        SourceDir = FindSourceRoot();
        TargetDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "ARTHA");
    }

    private string FindSourceRoot()
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        while (!string.IsNullOrEmpty(dir))
        {
            if (File.Exists(Path.Combine(dir, "ARTHA.exe")) || File.Exists(Path.Combine(dir, "server.js")))
            {
                return dir;
            }
            DirectoryInfo? parent = Directory.GetParent(dir);
            if (parent == null) break;
            dir = parent.FullName;
        }
        return AppDomain.CurrentDomain.BaseDirectory;
    }

    public async Task InstallAsync(IProgress<InstallerProgress> progress)
    {
        await Task.Run(() =>
        {
            progress.Report(new InstallerProgress(5, "Preparing setup environment..."));

            bool inPlace = string.Equals(
                Path.GetFullPath(SourceDir).TrimEnd('\\'),
                Path.GetFullPath(TargetDir).TrimEnd('\\'),
                StringComparison.OrdinalIgnoreCase);

            if (!Directory.Exists(TargetDir))
            {
                Directory.CreateDirectory(TargetDir);
            }

            if (!inPlace)
            {
                progress.Report(new InstallerProgress(15, "Copying core application binaries..."));

                // Copy single files
                string[] filesToCopy = { "ARTHA.exe", "server.bat", "server.js", "package.json", "package-lock.json", "LICENSE", "README.md" };
                foreach (string file in filesToCopy)
                {
                    string src = Path.Combine(SourceDir, file);
                    if (File.Exists(src))
                    {
                        File.Copy(src, Path.Combine(TargetDir, file), overwrite: true);
                    }
                }

                // Copy icon
                string srcIcon = Path.Combine(SourceDir, "launcher", "app-icon.ico");
                if (!File.Exists(srcIcon)) srcIcon = Path.Combine(SourceDir, "release-templates", "_system-scripts", "app-icon.ico");
                if (File.Exists(srcIcon))
                {
                    File.Copy(srcIcon, Path.Combine(TargetDir, "app-icon.ico"), overwrite: true);
                }

                progress.Report(new InstallerProgress(35, "Copying frontend distribution & assets..."));
                CopyDirectoryRecursive(Path.Combine(SourceDir, "dist"), Path.Combine(TargetDir, "dist"));
                CopyDirectoryRecursive(Path.Combine(SourceDir, "public"), Path.Combine(TargetDir, "public"));
                CopyDirectoryRecursive(Path.Combine(SourceDir, "scripts"), Path.Combine(TargetDir, "scripts"));
                CopyDirectoryRecursive(Path.Combine(SourceDir, "src"), Path.Combine(TargetDir, "src"));

                progress.Report(new InstallerProgress(65, "Setting up dependencies..."));
                if (Directory.Exists(Path.Combine(SourceDir, "node_modules")))
                {
                    progress.Report(new InstallerProgress(70, "Syncing node modules..."));
                    CopyDirectoryRecursive(Path.Combine(SourceDir, "node_modules"), Path.Combine(TargetDir, "node_modules"));
                }
            }
            else
            {
                progress.Report(new InstallerProgress(60, "Configuring existing installation in place..."));
                string srcIcon = Path.Combine(SourceDir, "launcher", "app-icon.ico");
                if (!File.Exists(srcIcon)) srcIcon = Path.Combine(SourceDir, "release-templates", "_system-scripts", "app-icon.ico");
                if (File.Exists(srcIcon))
                {
                    File.Copy(srcIcon, Path.Combine(TargetDir, "app-icon.ico"), overwrite: true);
                }
            }

            // Ensure data directory exists
            string dataDir = Path.Combine(TargetDir, "data");
            if (!Directory.Exists(dataDir)) Directory.CreateDirectory(dataDir);

            // Generate Uninstaller script
            progress.Report(new InstallerProgress(80, "Creating uninstaller..."));
            CreateUninstaller(TargetDir);

            // Create Shortcuts
            progress.Report(new InstallerProgress(90, "Creating Windows shortcuts..."));
            string exePath = Path.Combine(TargetDir, "ARTHA.exe");
            string iconPath = Path.Combine(TargetDir, "app-icon.ico");
            if (!File.Exists(iconPath)) iconPath = exePath;

            if (CreateDesktopShortcut)
            {
                string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                string lnk = Path.Combine(desktop, "ARTHA.lnk");
                CreateShortcut(lnk, exePath, TargetDir, iconPath, "ARTHA Accounting Software");
            }

            if (CreateStartMenuShortcut)
            {
                string programs = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs), "ARTHA");
                if (!Directory.Exists(programs)) Directory.CreateDirectory(programs);
                string lnk = Path.Combine(programs, "ARTHA.lnk");
                CreateShortcut(lnk, exePath, TargetDir, iconPath, "ARTHA Accounting Software");
            }

            // Register in Windows Add/Remove Programs (Registry)
            progress.Report(new InstallerProgress(95, "Registering Windows application..."));
            RegisterUninstall(TargetDir, exePath, iconPath);

            progress.Report(new InstallerProgress(100, "Setup complete!"));
        });
    }

    private static void CopyDirectoryRecursive(string source, string destination)
    {
        if (!Directory.Exists(source)) return;
        if (!Directory.Exists(destination)) Directory.CreateDirectory(destination);

        foreach (string file in Directory.GetFiles(source))
        {
            string destFile = Path.Combine(destination, Path.GetFileName(file));
            File.Copy(file, destFile, overwrite: true);
        }

        foreach (string dir in Directory.GetDirectories(source))
        {
            string destDir = Path.Combine(destination, Path.GetFileName(dir));
            CopyDirectoryRecursive(dir, destDir);
        }
    }

    private static void CreateShortcut(string shortcutPath, string targetPath, string workingDir, string iconPath, string description)
    {
        try
        {
            Type? shellType = Type.GetTypeFromProgID("WScript.Shell");
            if (shellType != null)
            {
                dynamic shell = Activator.CreateInstance(shellType)!;
                dynamic shortcut = shell.CreateShortcut(shortcutPath);
                shortcut.TargetPath = targetPath;
                shortcut.WorkingDirectory = workingDir;
                shortcut.Description = description;
                shortcut.IconLocation = iconPath + ",0";
                shortcut.Save();
            }
        }
        catch { }
    }

    private static void CreateUninstaller(string targetDir)
    {
        string uninstBat = Path.Combine(targetDir, "Uninstall.bat");
        string content = $@"@echo off
setlocal
title ARTHA - Uninstall

echo ========================================================
echo   ARTHA Accounting Software - Uninstaller
echo ========================================================
echo.
echo This will remove ARTHA application shortcuts and registry entries.
set /p CONFIRM=Do you want to proceed? (Y/N): 
if /i not ""%CONFIRM%""==""Y"" exit /b 0

:: Remove shortcuts
set ""DESKTOP_LNK=%USERPROFILE%\Desktop\ARTHA.lnk""
if exist ""%DESKTOP_LNK%"" del /f /q ""%DESKTOP_LNK%""

set ""SM_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\ARTHA""
if exist ""%SM_DIR%"" rmdir /s /q ""%SM_DIR%""

:: Clean registry
reg delete ""HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\ARTHA"" /f >nul 2>&1

echo.
echo [OK] Shortcuts and registration removed.
echo Note: Your invoices and data files in '%~dp0data' have been preserved.
echo If you wish to delete all files completely, delete the entire folder: '%~dp0'.
echo.
pause
";
        File.WriteAllText(uninstBat, content);
    }

    private static void RegisterUninstall(string targetDir, string exePath, string iconPath)
    {
        try
        {
            using var key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\ARTHA");
            if (key != null)
            {
                key.SetValue("DisplayName", "ARTHA Accounting Software");
                key.SetValue("DisplayVersion", "1.10.80");
                key.SetValue("Publisher", "VIJAYKRSHA.ONLINE");
                key.SetValue("DisplayIcon", iconPath);
                key.SetValue("InstallLocation", targetDir);
                key.SetValue("UninstallString", $"cmd.exe /c \"{Path.Combine(targetDir, "Uninstall.bat")}\"");
                key.SetValue("NoModify", 1, RegistryValueKind.DWord);
                key.SetValue("NoRepair", 1, RegistryValueKind.DWord);
            }
        }
        catch { }
    }
}

