#!/bin/sh
sudo apt-get install python-setuptools python-dev
easy_install pip
pip install -r requirements.txt

# Add PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/path/to/orion-ids

# Installing Graph Tools
# Visit http://graph-tool.skewed.de/download#debian for more information
deb http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe
deb-src http://downloads.skewed.de/apt/DISTRIBUTION DISTRIBUTION universe
sudo apt-get update
sudo apt-get install python-graph-tool