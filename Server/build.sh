#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

sudo apt install libmagic1
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

python manage.py collectstatic --no-input
python manage.py migrate