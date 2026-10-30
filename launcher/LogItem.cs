using System;
using System.Text.RegularExpressions;
using Brush = System.Windows.Media.Brush;
using Color = System.Windows.Media.Color;
using SolidColorBrush = System.Windows.Media.SolidColorBrush;

namespace ARTHA.Launcher;

public enum LogSource
{
    System,
    Backend,
    Frontend,
    Error
}

public class LogItem
{
    private static readonly Regex AnsiRegex = new(@"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", RegexOptions.Compiled);

    public DateTime Timestamp { get; }
    public LogSource Source { get; }
    public string Message { get; }
    public string FormattedTime => Timestamp.ToString("HH:mm:ss");

    public string SourceTag => Source switch
    {
        LogSource.Backend => "[BACKEND]",
        LogSource.Frontend => "[FRONTEND]",
        LogSource.Error => "[ERROR]",
        _ => "[SYSTEM]"
    };

    public Brush SourceColor => Source switch
    {
        LogSource.Backend => new SolidColorBrush(Color.FromRgb(56, 189, 248)),   // Cyan/Sky
        LogSource.Frontend => new SolidColorBrush(Color.FromRgb(74, 222, 128)),  // Emerald/Green
        LogSource.Error => new SolidColorBrush(Color.FromRgb(248, 113, 113)),   // Red
        _ => new SolidColorBrush(Color.FromRgb(251, 191, 36))                   // Amber
    };

    public Brush MessageColor => Source switch
    {
        LogSource.Error => new SolidColorBrush(Color.FromRgb(254, 202, 202)),
        LogSource.Frontend => new SolidColorBrush(Color.FromRgb(241, 245, 249)),
        LogSource.Backend => new SolidColorBrush(Color.FromRgb(241, 245, 249)),
        _ => new SolidColorBrush(Color.FromRgb(226, 232, 240))
    };

    public LogItem(LogSource source, string rawMessage)
    {
        Timestamp = DateTime.Now;
        Source = source;
        Message = CleanAnsi(rawMessage);
    }

    public static string CleanAnsi(string input)
    {
        if (string.IsNullOrEmpty(input)) return string.Empty;
        return AnsiRegex.Replace(input, string.Empty).TrimEnd();
    }

    public override string ToString()
    {
        return $"{FormattedTime} {SourceTag} {Message}";
    }
}
