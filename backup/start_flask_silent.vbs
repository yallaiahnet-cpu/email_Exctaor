' Silent launcher for Flask app (no command window)
' This version runs completely in the background
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
WshShell.CurrentDirectory = ScriptDir

' Run the Flask app silently (0 = hidden window)
' Use batch file if available, otherwise run Python directly
If fso.FileExists(ScriptDir & "\start_flask.bat") Then
    WshShell.Run "cmd /c start_flask.bat", 0, False
ElseIf fso.FileExists(ScriptDir & "\start_flask_simple.bat") Then
    WshShell.Run "cmd /c start_flask_simple.bat", 0, False
Else
    ' Fallback: run Python directly
    If fso.FileExists(ScriptDir & "\venv\Scripts\python.exe") Then
        WshShell.Run "cmd /c venv\Scripts\python.exe app.py", 0, False
    ElseIf fso.FileExists(ScriptDir & "\.venv\Scripts\python.exe") Then
        WshShell.Run "cmd /c .venv\Scripts\python.exe app.py", 0, False
    Else
        WshShell.Run "cmd /c python app.py", 0, False
    End If
End If

Set WshShell = Nothing
Set fso = Nothing


