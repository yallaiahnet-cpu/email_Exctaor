Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
WshShell.CurrentDirectory = ScriptDir

' Run the Flask app
' Try to use the batch file, or run Python directly
If fso.FileExists(ScriptDir & "\start_flask.bat") Then
    WshShell.Run "cmd /c start_flask.bat", 1, False
ElseIf fso.FileExists(ScriptDir & "\start_flask_simple.bat") Then
    WshShell.Run "cmd /c start_flask_simple.bat", 1, False
Else
    ' Fallback: run Python directly
    If fso.FileExists(ScriptDir & "\venv\Scripts\python.exe") Then
        WshShell.Run "cmd /c venv\Scripts\python.exe app.py", 1, False
    ElseIf fso.FileExists(ScriptDir & "\.venv\Scripts\python.exe") Then
        WshShell.Run "cmd /c .venv\Scripts\python.exe app.py", 1, False
    Else
        WshShell.Run "cmd /c python app.py", 1, False
    End If
End If

Set WshShell = Nothing
Set fso = Nothing


