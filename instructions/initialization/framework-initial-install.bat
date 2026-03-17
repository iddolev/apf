@echo off
REM Copies shared files from the agentic-programming folder to the user project.
REM Run from the project root (the parent of agentic-programming/).

set AP=agentic-programming

if not exist "%AP%" (
    echo Error: %AP% folder not found. Run this from the project root.
    exit /b 1
)

if not exist .claude\commands\apf mkdir .claude\commands\apf
if not exist .claude\scripts mkdir .claude\scripts

copy "%AP%\instructions\claude\commands\apf\start-agentic-framework.md" ".claude\commands\apf\start-agentic-framework.md" > NUL 2>&1
copy "%AP%\instructions\claude\commands\apf\update-agentic-framework.md" ".claude\commands\apf\update-agentic-framework.md" > NUL 2>&1
copy "%AP%\instructions\claude\scripts\update-agentic-framework.bat" ".claude\scripts\update-agentic-framework.bat" > NUL 2>&1
copy "%AP%\instructions\initialization\framework-initial-install.bat" "scripts\framework-initial-install.bat" > NUL 2>&1
copy "%AP%\.claude\commands\format-markdown.md" ".claude\commands\format-markdown.md" > NUL 2>&1
copy "%AP%\.claude\scripts\format_markdown.py" ".claude\scripts\format_markdown.py" > NUL 2>&1
copy "%AP%\.claude\scripts\log_agent_invocations.py" ".claude\scripts\log_agent_invocations.py" > NUL 2>&1

if not exist rules mkdir rules
copy "%AP%\instructions\rules\SOFTWARE-ENGINEERING-PRINCIPLES.md" "rules\SOFTWARE-ENGINEERING-PRINCIPLES.md" > NUL 2>&1

if not exist STATE mkdir STATE
if not exist "STATE\FRAMEWORK-STATE.yaml" copy "%AP%\instructions\state\FRAMEWORK-STATE-template.yaml" "STATE\FRAMEWORK-STATE.yaml" > NUL 2>&1

if not exist scripts mkdir scripts
copy "%AP%\.claude\scripts\log_hook_event.py" ".claude\scripts\log_hook_event.py" > NUL 2>&1
copy "%AP%\instructions\initialization\install_hook_event_logger.py" "scripts\install_hook_event_logger.py" > NUL 2>&1
python scripts\install_hook_event_logger.py

echo Done: Shared files copied to the project, and hooks event logger installed (turned off).
