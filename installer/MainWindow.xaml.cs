using System;
using System.Diagnostics;
using System.IO;
using System.Windows;
using Microsoft.Win32;

namespace ARTHA.Installer;

public partial class MainWindow : Window
{
    private readonly InstallerEngine _engine;

    public MainWindow()
    {
        InitializeComponent();
        _engine = new InstallerEngine();
    }

    private void Window_Loaded(object sender, RoutedEventArgs e)
    {
        TxtTargetPath.Text = _engine.TargetDir;
    }

    private void BtnBrowse_Click(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFolderDialog
        {
            Title = "Select ARTHA Installation Directory",
            InitialDirectory = TxtTargetPath.Text
        };

        if (dialog.ShowDialog() == true)
        {
            TxtTargetPath.Text = dialog.FolderName;
            ChkInPlace.IsChecked = false;
        }
    }

    private void ChkInPlace_Checked(object sender, RoutedEventArgs e)
    {
        TxtTargetPath.Text = _engine.SourceDir;
        TxtTargetPath.IsEnabled = false;
    }

    private void ChkInPlace_Unchecked(object sender, RoutedEventArgs e)
    {
        TxtTargetPath.Text = _engine.TargetDir;
        TxtTargetPath.IsEnabled = true;
    }

    private async void BtnInstall_Click(object sender, RoutedEventArgs e)
    {
        string target = TxtTargetPath.Text.Trim();
        if (string.IsNullOrEmpty(target))
        {
            MessageBox.Show("Please choose an installation folder.", "Invalid Folder", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        _engine.TargetDir = target;
        _engine.CreateDesktopShortcut = ChkDesktopShortcut.IsChecked == true;
        _engine.CreateStartMenuShortcut = ChkStartMenuShortcut.IsChecked == true;
        _engine.LaunchAfterInstall = ChkAutoLaunch.IsChecked == true;

        PanelStepOptions.Visibility = Visibility.Collapsed;
        PanelStepProgress.Visibility = Visibility.Visible;
        BtnInstall.Visibility = Visibility.Collapsed;
        BtnCancel.IsEnabled = false;

        var progress = new Progress<InstallerProgress>(p =>
        {
            ProgressBarInstall.Value = p.Percentage;
            TxtPercent.Text = $"{p.Percentage}%";
            TxtProgressStatus.Text = p.Status;
        });

        try
        {
            await _engine.InstallAsync(progress);

            PanelStepProgress.Visibility = Visibility.Collapsed;
            PanelStepFinished.Visibility = Visibility.Visible;
            BtnCancel.Visibility = Visibility.Collapsed;
            BtnFinish.Visibility = Visibility.Visible;
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Installation encountered an error: {ex.Message}", "Installation Error", MessageBoxButton.OK, MessageBoxImage.Error);
            PanelStepProgress.Visibility = Visibility.Collapsed;
            PanelStepOptions.Visibility = Visibility.Visible;
            BtnInstall.Visibility = Visibility.Visible;
            BtnCancel.IsEnabled = true;
        }
    }

    private void BtnFinish_Click(object sender, RoutedEventArgs e)
    {
        if (_engine.LaunchAfterInstall)
        {
            string exe = Path.Combine(_engine.TargetDir, "ARTHA.exe");
            if (File.Exists(exe))
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = exe,
                    WorkingDirectory = _engine.TargetDir,
                    UseShellExecute = true
                });
            }
        }
        Close();
    }

    private void BtnCancel_Click(object sender, RoutedEventArgs e)
    {
        Close();
    }
}

