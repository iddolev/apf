@echo off
echo.
echo -----------------------------------------------------------------------
echo This is a script for fetching the starting-point.bat script,
echo to help you set up agentic programming in a new project.
echo -----------------------------------------------------------------------
echo.

if "%GITLAB_TOKEN_EVOLUTION%"=="" (
      echo Error: Environment variable GITLAB_TOKEN_EVOLUTION is not set.
      echo Modify this script to use the Windows environment variable where you stored your gitlab personal access token.
      echo.
      echo If you don't have such a token yet, login to your gitlab Evolution account,
      echo click on your avatar > Preferences > Access Tokens > Add new tokens, create a token, copy it,
      echo and then in Windows environment variables set GITLAB_TOKEN_EVOLUTION to equal this token value.
      echo Then run this script again.
      exit /b 1
  )


curl -s --header "PRIVATE-TOKEN: %GITLAB_TOKEN_EVOLUTION%" "https://gitlab.com/api/v4/projects/80018565/repository/files/scripts%%2Fstarting-point.bat/raw?ref=main" -o starting-point.bat

echo Now you should have the file starting-point.bat.
echo I'm now trying to run it.

.\starting-point.bat
