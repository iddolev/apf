@echo off
REM This script is to be used only by a user once to setup the agentic programming framework in their project.
REM Therefore, it should NOT be copied to the user project's scripts folder.
REM Do not run it when developing the agentic-programming project itself.

echo Run this script just once to initialize the agentic programming framework for your project.

if exist agentic-programming (
    echo.
    echo Error: agentic-programming folder already exists.
    echo To update, run this command in Claude Code: /update-agentic-framework
    exit /b 1
)

echo.
echo Cloning the agentic programming framework into agentic-programming/ ...

git clone git@gitlab.com:claude-code-experiments/agentic-programming.git > NUL 2>&1
call agentic-programming\instructions\initialization\framework-initial-install.bat  > NUL 2>&1

echo.
echo Done.
echo Now you can run Claude Code (using: "claude"), and run the command: /start-agentic-framework
echo.
