@echo off
echo.
echo -----------------------------------------------------------------------
echo This is a script for fetching markdown instructions files,
echo which will allow you to instruct an LLM (e.g. in Cursor or Claude Code)
echo to help you set up a new project with agentic programming.
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

echo Getting the zipped instructions folder...
curl -s --header "PRIVATE-TOKEN: %GITLAB_TOKEN_EVOLUTION%" "https://gitlab.com/api/v4/projects/80018565/repository/archive.zip?path=instructions&ref=main" -o instructions.zip
echo Unzipping...
tar -xf instructions.zip --strip-components=1
echo Deleting instructions.zip
del instructions.zip

echo.
echo Now you should have the instruction files under the "instructions" folder.
echo In the Cursor IDE, choose the Claude Sonnet model, and give the prompt:
echo "Follow the instructions in @starting-point.md"
echo Or run Claude Code (using "claude") and give it the same prompt.
