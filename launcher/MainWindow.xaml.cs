using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Media;
using Microsoft.Win32;
using Forms = System.Windows.Forms;
using WpfMessageBox = System.Windows.MessageBox;
using WpfClipboard = System.Windows.Clipboard;
using WpfRadioButton = System.Windows.Controls.RadioButton;
using WpfSaveFileDialog = Microsoft.Win32.SaveFileDialog;

namespace ARTHA.Launcher;

public partial class MainWindow : Window
{
    private readonly ServerManager _serverManager;
    private readonly ObservableCollection<LogItem> _allLogs = new();
    private ICollectionView? _logView;
    private Forms.NotifyIcon? _notifyIcon;
    private string _currentFilterTag = "All";
    private string _searchFilter = "";
    private bool _isExplicitExit = false;

    public MainWindow()
    {
        InitializeComponent();
        _serverManager = new ServerManager();
        _serverManager.LogReceived += OnLogReceived;
        _serverManager.StatusChanged += OnStatusChanged;
    }

    private async void Window_Loaded(object sender, RoutedEventArgs e)
    {
        TxtDirectory.Text = _serverManager.RootDir;

        // Set up CollectionView for filtering and virtualized performance
        _logView = CollectionViewSource.GetDefaultView(_allLogs);
        _logView.Filter = FilterLogPredicate;
        LogListView.ItemsSource = _logView;

        SetupSystemTray();

        // Start services automatically
        await _serverManager.StartAsync();
    }

    private void SetupSystemTray()
    {
        try
        {
            _notifyIcon = new Forms.NotifyIcon
            {
                Text = "ARTHA Accounting Software",
                Visible = true
            };

            string iconPath = Path.Combine(_serverManager.RootDir, "release-templates", "_system-scripts", "app-icon.ico");
            if (!File.Exists(iconPath))
            {
                iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "app-icon.ico");
            }

            if (File.Exists(iconPath))
            {
                _notifyIcon.Icon = new System.Drawing.Icon(iconPath);
            }
            else
            {
                _notifyIcon.Icon = System.Drawing.SystemIcons.Application;
            }

            var contextMenu = new Forms.ContextMenuStrip();
            contextMenu.Items.Add("Open ARTHA Console", null, (s, e) => RestoreWindow());
            contextMenu.Items.Add("Open App in Browser", null, (s, e) => OpenBrowser());
            contextMenu.Items.Add(new Forms.ToolStripSeparator());
            contextMenu.Items.Add("Restart Services", null, async (s, e) => await _serverManager.RestartAsync());
            contextMenu.Items.Add(new Forms.ToolStripSeparator());
            contextMenu.Items.Add("Exit ARTHA", null, (s, e) =>
            {
                _isExplicitExit = true;
                Close();
            });

            _notifyIcon.ContextMenuStrip = contextMenu;
            _notifyIcon.DoubleClick += (s, e) => RestoreWindow();
        }
        catch (Exception ex)
        {
            _serverManager.AddLog(LogSource.Error, $"System tray setup warning: {ex.Message}");
        }
    }

    private void RestoreWindow()
    {
        Show();
        WindowState = WindowState.Normal;
        Activate();
        Focus();
    }

    private void OpenBrowser()
    {
        try
        {
            // Open frontend if running, or backend port
            int port = _serverManager.IsFrontendRunning ? _serverManager.FrontendPort : _serverManager.BackendPort;
            string url = $"http://localhost:{port}/";
            Process.Start(new ProcessStartInfo
            {
                FileName = url,
                UseShellExecute = true
            });
        }
        catch (Exception ex)
        {
            _serverManager.AddLog(LogSource.Error, $"Could not open browser: {ex.Message}");
        }
    }

    private void OnLogReceived(LogItem item)
    {
        Dispatcher.BeginInvoke(() =>
        {
            // Keep memory bounded to 15,000 entries
            if (_allLogs.Count > 15000)
            {
                _allLogs.RemoveAt(0);
            }

            _allLogs.Add(item);

            if (ChkAutoScroll?.IsChecked == true && LogScrollViewer != null)
            {
                LogScrollViewer.ScrollToEnd();
            }
        });
    }

    private void OnStatusChanged()
    {
        Dispatcher.BeginInvoke(() =>
        {
            // Update Backend Status
            if (_serverManager.IsBackendHealthy)
            {
                BackendDot.Fill = (SolidColorBrush)FindResource("AccentGreen");
                TxtBackendStatus.Text = $"Running (:{_serverManager.BackendPort})";
            }
            else if (_serverManager.IsBackendRunning)
            {
                BackendDot.Fill = (SolidColorBrush)FindResource("AccentAmber");
                TxtBackendStatus.Text = $"Starting (:{_serverManager.BackendPort})...";
            }
            else
            {
                BackendDot.Fill = (SolidColorBrush)FindResource("AccentRed");
                TxtBackendStatus.Text = "Stopped";
            }

            // Update Frontend Status
            if (_serverManager.IsFrontendHealthy)
            {
                FrontendDot.Fill = (SolidColorBrush)FindResource("AccentGreen");
                TxtFrontendStatus.Text = $"Running (:{_serverManager.FrontendPort})";
            }
            else if (_serverManager.IsFrontendRunning)
            {
                FrontendDot.Fill = (SolidColorBrush)FindResource("AccentAmber");
                TxtFrontendStatus.Text = $"Starting (:{_serverManager.FrontendPort})...";
            }
            else
            {
                FrontendDot.Fill = (SolidColorBrush)FindResource("AccentRed");
                TxtFrontendStatus.Text = "Stopped";
            }

            // Update Start/Stop button
            bool anyRunning = _serverManager.IsBackendRunning || _serverManager.IsFrontendRunning;
            if (anyRunning)
            {
                BtnToggleService.Background = (SolidColorBrush)FindResource("AccentRed");
                TxtToggleService.Text = "⏹ Stop";
            }
            else
            {
                BtnToggleService.Background = (SolidColorBrush)FindResource("AccentGreen");
                TxtToggleService.Text = "▶ Start";
            }
        });
    }

    private bool FilterLogPredicate(object obj)
    {
        if (obj is not LogItem log) return false;

        // Tag filter
        if (_currentFilterTag != "All")
        {
            if (_currentFilterTag == "Backend" && log.Source != LogSource.Backend) return false;
            if (_currentFilterTag == "Frontend" && log.Source != LogSource.Frontend) return false;
            if (_currentFilterTag == "Error" && log.Source != LogSource.Error) return false;
            if (_currentFilterTag == "System" && log.Source != LogSource.System) return false;
        }

        // Search text filter
        if (!string.IsNullOrWhiteSpace(_searchFilter))
        {
            return log.Message.Contains(_searchFilter, StringComparison.OrdinalIgnoreCase) ||
                   log.SourceTag.Contains(_searchFilter, StringComparison.OrdinalIgnoreCase);
        }

        return true;
    }

    private void FilterChanged(object sender, RoutedEventArgs e)
    {
        if (sender is WpfRadioButton rb)
        {
            _currentFilterTag = rb.Tag?.ToString() ?? "All";
            _logView?.Refresh();
            if (ChkAutoScroll?.IsChecked == true && LogScrollViewer != null)
            {
                LogScrollViewer.ScrollToEnd();
            }
        }
    }

    private void TxtSearch_TextChanged(object sender, TextChangedEventArgs e)
    {
        if (TxtSearch == null) return;
        _searchFilter = TxtSearch.Text.Trim();
        _logView?.Refresh();
        if (ChkAutoScroll?.IsChecked == true && LogScrollViewer != null)
        {
            LogScrollViewer.ScrollToEnd();
        }
    }

    private void BtnOpenBrowser_Click(object sender, RoutedEventArgs e)
    {
        OpenBrowser();
    }

    private async void BtnRestart_Click(object sender, RoutedEventArgs e)
    {
        BtnRestart.IsEnabled = false;
        try
        {
            await _serverManager.RestartAsync();
        }
        finally
        {
            BtnRestart.IsEnabled = true;
        }
    }

    private async void BtnToggleService_Click(object sender, RoutedEventArgs e)
    {
        BtnToggleService.IsEnabled = false;
        try
        {
            if (_serverManager.IsBackendRunning || _serverManager.IsFrontendRunning)
            {
                await _serverManager.StopAsync();
            }
            else
            {
                await _serverManager.StartAsync();
            }
        }
        finally
        {
            BtnToggleService.IsEnabled = true;
        }
    }

    private void BtnCopy_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var sb = new StringBuilder();
            foreach (var item in _allLogs)
            {
                if (FilterLogPredicate(item))
                {
                    sb.AppendLine(item.ToString());
                }
            }
            WpfClipboard.SetText(sb.ToString());
            _serverManager.AddLog(LogSource.System, $"Copied logs to clipboard.");
        }
        catch (Exception ex)
        {
            WpfMessageBox.Show($"Failed to copy logs: {ex.Message}", "Clipboard Error", MessageBoxButton.OK, MessageBoxImage.Warning);
        }
    }

    private void BtnClear_Click(object sender, RoutedEventArgs e)
    {
        _allLogs.Clear();
        _serverManager.AddLog(LogSource.System, "Log console cleared.");
    }

    private void BtnExport_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var sfd = new WpfSaveFileDialog
            {
                Filter = "Log files (*.log)|*.log|Text files (*.txt)|*.txt|All files (*.*)|*.*",
                FileName = $"ARTHA_Logs_{DateTime.Now:yyyyMMdd_HHmmss}.log",
                Title = "Export ARTHA Logs"
            };

            if (sfd.ShowDialog() == true)
            {
                var sb = new StringBuilder();
                foreach (var item in _allLogs)
                {
                    sb.AppendLine(item.ToString());
                }
                File.WriteAllText(sfd.FileName, sb.ToString(), Encoding.UTF8);
                _serverManager.AddLog(LogSource.System, $"Logs successfully exported to: {sfd.FileName}");
            }
        }
        catch (Exception ex)
        {
            WpfMessageBox.Show($"Export failed: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    private void TxtDirectory_MouseDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
    {
        try
        {
            Process.Start("explorer.exe", $"\"{_serverManager.RootDir}\"");
        }
        catch { }
    }

    private void Window_StateChanged(object sender, EventArgs e)
    {
        if (WindowState == WindowState.Minimized && ChkMinimizeToTray.IsChecked == true)
        {
            Hide();
            _notifyIcon?.ShowBalloonTip(
                2000,
                "ARTHA Server Running",
                "Frontend and Backend are running in the background. Double-click to open ARTHA Console.",
                Forms.ToolTipIcon.Info
            );
        }
    }

    private async void Window_Closing(object sender, CancelEventArgs e)
    {
        if (!_isExplicitExit && ChkMinimizeToTray.IsChecked == true)
        {
            e.Cancel = true;
            WindowState = WindowState.Minimized;
            return;
        }

        // Clean termination
        _notifyIcon?.Dispose();
        await _serverManager.StopAsync();
    }
}
