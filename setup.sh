#!/bin/bash

# Get packages for re-building Banshee
sudo apt-get install debian-keyring
sudo apt-get install devscripts

# Get dependencies
sudo apt-get install git-core autoconf automake libtool intltool gcc make libgconf2.0-cil-dev libgconf2-dev
sudo apt-get build-dep banshee

# Get source and patch
apt-get source banshee=2.6.2-3
cd banshee-2.6.2
patch -p0 < ../musiccube.patch

# Re-build Banshee and install
debchange -n "Applied patches for Banshee MusicCube"
debuild -b -uc -us
cd ..
sudo dpkg -i banshee_2.6.2-3.1_amd64.deb

# Install LLVM 3.7
wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
grep llvm.org /etc/apt/sources.list || sudo echo deb http://apt.llvm.org/jessie/ llvm-toolchain-jessie-3.7 main >> /etc/apt/sources.list
sudo apt-get update
sudo apt-get install libedit-dev
sudo apt-get install llvm-3.7-dev
export LLVM_CONFIG=$(which llvm-config-3.7)

# Install audio video converter
sudo apt-get install libav-tools 

# Install python tools
sudo apt-get install python-dev
sudo apt-get install python-gconf
sudo apt-get install python-pip
sudo apt-get install python-matplotlib

# Install numba
pip install --user enum34
pip install --user numba

# Compile and install
./autogen.sh
make
sudo cp lib/Banshee.MusicCube.dll /usr/lib/banshee/Extensions/
