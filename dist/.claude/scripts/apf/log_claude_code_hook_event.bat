@echo off
set "FLAG_FILE=.apf\.log_claude_code_hook_event"
set /p FLAG=<"%FLAG_FILE%"
if "%FLAG%"=="on" (
    echo HI1111
    echo hi2222 1>&2
    python "%~dp0log_claude_code_hook_event.py"
) else (
    echo hi3333
    echo hi4444 1>&2
)
