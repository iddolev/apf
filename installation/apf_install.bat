@echo off
REM This is the file to share with anyone who wants to install APF in their project folder

if not exist ".installation" mkdir ".installation"

curl -sL -o ".installation\apf_install.py" https://raw.githubusercontent.com/iddolev/apf/main/installation/apf_install.py

for %%a in (%*) do if "%%a"=="--fetch" (
    echo Fetched apf_install.py
    exit /b 0
)

pip install pyyaml ruamel.yaml
python ".installation\apf_install.py" %*
