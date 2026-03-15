@echo off
REM Appends a record to HISTORY.jsonl in the project root.
REM Usage: .claude\scripts\history-add.bat <actor> <event_type> <message>
REM   actor      — name of the agent or process (e.g. "backend-specialist", "starting-point")
REM   event_type — one of:
REM                agent-started:  when an agent is invoked
REM                agent-finished: when an agent finishes to run
REM                agent-mid:      and important step done during the session of an agent
REM                event:          other events
REM   message    — short description of what happened

echo CALLED history-add %*

if "%~1"=="" (
    echo Usage: history-add.bat ^<actor^> ^<event_type^> ^<message^> >&2
    exit /b 1
)
if "%~2"=="" (
    echo Usage: history-add.bat ^<actor^> ^<event_type^> ^<message^> >&2
    exit /b 1
)
if "%~3"=="" (
    echo Usage: history-add.bat ^<actor^> ^<event_type^> ^<message^> >&2
    exit /b 1
)

set "actor=%~1"
set "event_type=%~2"

REM Combine all remaining arguments (from 3rd onward) as the message
shift
shift
set "message=%~1"
shift
:argloop
if "%~1"=="" goto :done
set "message=%message% %~1"
shift
goto :argloop
:done

REM Get UTC timestamp
for /f "tokens=*" %%T in ('powershell -nologo -noprofile -command "[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')"') do set "timestamp=%%T"

>> STATE\HISTORY.jsonl echo {"timestamp":"%timestamp%","actor":"%actor%","event_type":"%event_type%","message":"%message%"}
