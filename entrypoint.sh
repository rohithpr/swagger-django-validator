#!/bin/sh -l

# Install dependencies of the project being checked to ensure that django.setup() runs correctly.
pip install -r requirements.txt

# Install pyyaml to read the Swagger file.
pip install pyyaml

# Copy required files into the workspace.
# TODO: Copying it to the workspace from the Dockerfile itself fails. Why?
# Perhaps something to do with the `checkout` action?
cp /controller.py /github/workspace/controller.py

# Validate away
python /github/workspace/controller.py
