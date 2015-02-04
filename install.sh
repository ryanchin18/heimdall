#!/bin/sh
sudo apt-get install python-setuptools python-dev
easy_install pip
pip install -r requirements.txt

# Add PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/path/to/orion-ids