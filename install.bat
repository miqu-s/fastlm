@echo off

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install --upgrade setuptools

echo FastLM dependencies have been successfully installed.

python main.py

echo FastLM has been successfully installed and executed.

pause
