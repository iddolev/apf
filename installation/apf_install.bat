@echo off
REM This is the file to share with anyone who wants to install APF in their project folder

if not exist ".apf_install" mkdir ".apf_install"

curl -sL -o ".apf_install\apf_install.py" https://raw.githubusercontent.com/iddolev/apf/main/installation/apf_install.py

for %%a in (%*) do if "%%a"=="--fetch" (
    echo Fetched apf_install.py
    exit /b 0
)

pip install pyyaml ruamel.yaml
python ".apf_install\apf_install.py" %*
