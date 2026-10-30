using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows;

namespace ARTHA.Launcher;

public partial class App : System.Windows.Application
{
    private static Mutex? _mutex;
    private const string MutexName = "ARTHA_BILLING_LAUNCHER_SINGLE_INSTANCE_MUTEX";

    [DllImport("user32.dll")]
    private static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    private const int SW_RESTORE = 9;

    private void Application_Startup(object sender, StartupEventArgs e)
    {
        _mutex = new Mutex(true, MutexName, out bool isNew);

        if (!isNew)
        {
            // Activate existing instance
            Process current = Process.GetCurrentProcess();
            foreach (Process proc in Process.GetProcessesByName(current.ProcessName))
            {
                if (proc.Id != current.Id && proc.MainWindowHandle != IntPtr.Zero)
                {
                    ShowWindow(proc.MainWindowHandle, SW_RESTORE);
                    SetForegroundWindow(proc.MainWindowHandle);
                    break;
                }
            }
            Current.Shutdown();
            return;
        }

        var mainWindow = new MainWindow();
        mainWindow.Show();
    }

    private void Application_Exit(object sender, ExitEventArgs e)
    {
        _mutex?.ReleaseMutex();
        _mutex?.Dispose();
    }
}
