#!/bin/sh -l

# Install dependencies of the project being checked to ensure that django.setup() runs correctly.
pip install -r requirements.txt

# Install pyyaml to read the Swagger file.
pip install pyyaml

# Validate away
python /controller.py
