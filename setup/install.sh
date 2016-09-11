#!/bin/bash
#################################################
#################################################
#       Environment Setup for Heimdall          #
#################################################
#################################################


#-----------------------------------------------#
#               Define Variables                #
#-----------------------------------------------#
# Get this script's location
HEIMDALL_PATH=$( cd $(dirname $0) ; cd ../ ; pwd -P )

# Get Ubuntu DISTRIBUTION
DISTRIBUTION=$(lsb_release -s -c)

# List of apt-get applications to install
LIST_OF_APPS="
    build-essential
    python-dev
    python-setuptools
    python-software-properties
    redis-server
    libatlas-dev
    libatlas3gf-base
	expat
	libsparsehash-dev
	gtk+3
	libboost-all-dev
	graphviz
	libcairo2-dev
	python-pip
	python-matplotlib
	gfortran
	libopenblas-dev
	liblapack-dev
	libcgal-dev
	python-numpy
	python2.7-config
	python-cairo
	python-scipy
    "

# List of easy install applications to install
LIST_OF_EASY_INSTALL="
    pip
    "


#-----------------------------------------------#
#          Add Enrivonment Variable             #
#-----------------------------------------------#
if [[ "${PYTHONPATH}" =~ "${HEIMDALL_PATH}" ]]; then
    echo "PYTHONPATH already exists"
else
    echo "export PYTHONPATH=$PYTHONPATH:${HEIMDALL_PATH}" >> ~/.bashrc
    . ~/.bashrc
fi

#-----------------------------------------------#
#          Add repositories                     #
#-----------------------------------------------#
sudo add-apt-repository -y ppa:rwky/redis
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test


#-----------------------------------------------#
#          Install apt-get Packages             #
#-----------------------------------------------#
# Install apt-get packages
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y ${LIST_OF_APPS}

#-----------------------------------------------#
#           Installing Graph Tools              #
#-----------------------------------------------#
# Visit http://graph-tool.skewed.de/download#debian for more information
# Add PGP key
sudo apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25
# sudo apt-key add ${HEIMDALL_PATH}/setup/graph_tool.key

# Create a list file
echo "deb http://downloads.skewed.de/apt/${DISTRIBUTION} ${DISTRIBUTION} universe" | sudo tee /etc/apt/sources.list.d/graph_tool.list
echo "deb-src http://downloads.skewed.de/apt/${DISTRIBUTION} ${DISTRIBUTION} universe" | sudo tee -a /etc/apt/sources.list.d/graph_tool.list

sudo apt-get update
sudo apt-get -y --force-yes install python-graph-tool

#-----------------------------------------------#
#           Installing python packages          #
#-----------------------------------------------#
# Install easy_install packages
sudo easy_install-2.7 ${LIST_OF_EASY_INSTALL}

# Install required python libraries
sudo pip install -r ${HEIMDALL_PATH}/requirements.txt


#-----------------------------------------------#
#       Finalize Environment Installation       #
#-----------------------------------------------#
# Back to script dir
cd ${HEIMDALL_PATH}

# Environment setup completed
echo "***********************************************************************"
echo "*****             Environment Installation Completed              *****"
echo "***********************************************************************"