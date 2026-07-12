#!/bin/bash
set -e

echo "> Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip install markdown

echo "> Downloading Tailwind CSS CLI..."
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss

echo "> Fetching data..."
python3 fetch_data.py

echo "> Building static site..."
python3 build_site.py
