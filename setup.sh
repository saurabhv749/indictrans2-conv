#!/usr/bin/env bash
set -e
echo "Installing core NLP dependencies..."
python3 -m pip install nltk sacremoses pandas regex mock transformers==4.53.2 mosestokenizer

echo "Downloading NLTK punkt tokenizer..."
python3 -c "import nltk; nltk.download('punkt')"

echo "Installing acceleration and dataset libraries..."
python3 -m pip install bitsandbytes scipy accelerate datasets

echo "Installing sentencepiece..."
python3 -m pip install sentencepiece

echo "Upgrading torchao..."
python3 -m pip install --upgrade 'torchao>=0.16.0'

echo "Installing local indictranstools package in editable mode..."
echo "Installing local indictranstools package in editable mode..."
cd indictranstools && python3 -m pip install --editable ./
cd ..

echo "Downloading sample dataset..."
wget -q -O en-indic-exp.zip \
https://github.com/saurabhv749/indictrans2-conv/raw/refs/heads/main/dataset/en-indic-exp.zip
echo "Extracting sample dataset..."
unzip -o -d ./sample-dataset en-indic-exp.zip
rm -rf en-indic-exp.zip

echo "Setup complete."
echo "Restart the runtime."
