#!/bin/bash

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install cmake

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt

echo "FastLM dependencies have been successfully installed."

python3 main.py

echo "FastLM has been successfully installed and executed."