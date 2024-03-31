#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

apt-get install libmagic1
apt install tesseract-ocr
apt install libtesseract-dev

python manage.py collectstatic --no-input
python manage.py migrate