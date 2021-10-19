#!/bin/bash

INST_DIR="/tmp/assistant"
if [ -f /etc/os-release ]; then
    . /etc/os-release
fi
ID=$(echo "$ID" | sed -r 's/\"//g')
VER=$(echo "$VERSION_ID" | sed -r 's/\"//g')
VER_TEMP=$(echo "$VER" | sed -r 's/\..*//')

if [[ ($ID == "altlinux" || $ID == "centos") && $VER_TEMP == "7" ]]
then
    export LD_LIBRARY_PATH=$INST_DIR/lib
fi

if [[ $ID == "altlinux" && $VER_TEMP == "9" ]]
then 
    ln -s $INST_DIR/share/fonts/99-fonts-safib.conf /etc/fonts/conf.d/99-fonts-safib-prtbl.conf
    $INST_DIR/bin/assistant
    rm /etc/fonts/conf.d/99-fonts-safib-prtbl.conf
else
    $INST_DIR/bin/assistant
fi

exit 0