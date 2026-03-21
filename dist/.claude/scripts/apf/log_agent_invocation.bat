@echo off
set "FLAG_FILE=.apf\.log_agent_invocation"
set /p FLAG=<"%FLAG_FILE%"
if "%FLAG%"=="on" (
    python "%~dp0log_agent_invocation.py" %*
) else (
    echo.
)
