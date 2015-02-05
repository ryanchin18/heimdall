#!/bin/bash
#################################################
#################################################
#       Environmet Setup for orion-ids          #
#################################################
#################################################


#-----------------------------------------------#
#               Define Variables                #
#-----------------------------------------------#
# Get this script's location
ORION_PATH=$( cd $(dirname $0) ; cd ../ ; pwd -P )

# Get Ubuntu DISTRIBUTION
DISTRIBUTION=$(lsb_release -s -c)

# List of apt-get applications to install
LIST_OF_APPS="
    python-setuptools
    python-dev
    python-graph-tool
    "

# List of easy install applications to install
LIST_OF_EASY_INSTALL="
    pip
    "


#-----------------------------------------------#
#          Add Enrivonment Variable             #
#-----------------------------------------------#
echo "export PYTHONPATH=$PYTHONPATH:${ORION_PATH}" >> ~/.bashrc
source ~/.bashrc


#-----------------------------------------------#
#           Installing Graph Tools              #
#-----------------------------------------------#
# Visit http://graph-tool.skewed.de/download#debian for more information

# Create a list file
echo "deb http://downloads.skewed.de/apt/${DISTRIBUTION} ${DISTRIBUTION} universe" | sudo tee /etc/apt/sources.list.d/graph_tool.list
echo "deb-src http://downloads.skewed.de/apt/${DISTRIBUTION} ${DISTRIBUTION} universe" | sudo tee -a /etc/apt/sources.list.d/graph_tool.list

# Add PGP key
sudo apt-key add ${ORION_PATH}/setup/graph_tool.key


#-----------------------------------------------#
#          Install defined Packages             #
#-----------------------------------------------#
# Install apt-get packages
sudo apt-get update
sudo apt-get install -y ${LIST_OF_APPS}

# Install easy_install packages
sudo easy_install-2.7 ${LIST_OF_EASY_INSTALL}

# Install required python libraries
sudo pip install -r ${ORION_PATH}/requirements.txt


#-----------------------------------------------#
#       Finalize Environment Installation       #
#-----------------------------------------------#
# Back to script dir
cd ${ORION_PATH}

# Environment setup completed
echo "***********************************************************************"
echo "*****             Environment Installation Completed              *****"
echo "***********************************************************************"