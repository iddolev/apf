@echo off
REM This is the file to share with anyone who wants to install APF in their project folder

curl -sL -o apf_install.py https://raw.githubusercontent.com/iddolev/apf/main/installation/apf_install.py

for %%a in (%*) do if "%%a"=="--import" exit /b 0

python apf_install.py %*
