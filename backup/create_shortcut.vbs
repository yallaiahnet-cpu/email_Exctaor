' Script to create a desktop shortcut with custom icon for Flask app
Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
DesktopPath = WshShell.SpecialFolders("Desktop")

' Create shortcut
Set Shortcut = WshShell.CreateShortcut(DesktopPath & "\Start Flask App.lnk")
Shortcut.TargetPath = "wscript.exe"
Shortcut.Arguments = """" & ScriptDir & "\start_flask.vbs"""
Shortcut.WorkingDirectory = ScriptDir
Shortcut.Description = "Start Email Notifications Flask Server"
Shortcut.WindowStyle = 1

' Try to set a custom icon (you can change this to any .ico file)
' Option 1: Use Python icon if available
If fso.FileExists("C:\Program Files\Python3x\python.exe") Then
    Shortcut.IconLocation = "C:\Program Files\Python3x\python.exe,0"
ElseIf fso.FileExists("C:\Python3x\python.exe") Then
    Shortcut.IconLocation = "C:\Python3x\python.exe,0"
Else
    ' Option 2: Use a web/network icon from Windows
    Shortcut.IconLocation = "shell32.dll,13"  ' Network/Web icon
End If

Shortcut.Save

WScript.Echo "Shortcut created on Desktop: 'Start Flask App'" & vbCrLf & vbCrLf & _
             "You can:" & vbCrLf & _
             "1. Right-click the shortcut → Properties" & vbCrLf & _
             "2. Click 'Change Icon...' to set a custom icon" & vbCrLf & _
             "3. Browse to any .ico file or use icons from:" & vbCrLf & _
             "   - C:\Windows\System32\shell32.dll" & vbCrLf & _
             "   - C:\Windows\System32\imageres.dll"

Set Shortcut = Nothing
Set WshShell = Nothing
Set fso = Nothing

