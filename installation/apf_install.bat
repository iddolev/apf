@echo off
REM This is the file to share with anyone who wants to install APF in their project folder

curl -sL -o apf_install.py https://raw.githubusercontent.com/iddolev/apf/main/installation/apf_install.py

for %%a in (%*) do if "%%a"=="--fetch" (
    echo Fetched apf_install.py
    exit /b 0
)

pip install ruamel.yaml
python apf_install.py %*
