#!/bin/bash

INST_DIR="/opt/assistant"

export LD_LIBRARY_PATH=$INST_DIR/lib

sleep 2s

echo | tee -a /opt/assistant/log/daemon.log
echo "$(date) Starting Assistant..." | tee -a /opt/assistant/log/daemon.log

if [[ -z $XAUTHORITY ]]
then
    echo "Finding current xauthority" | tee -a /opt/assistant/log/daemon.log
    XAUTHORITY=$(find /var/run/xauth/ -name "*" -type f -mmin +0 -printf "%Ts %p\n" | sort -n | tail -1 | sed -r -e 's/^[0-9]+ //')
    DISPLAY=$(ps -u "$(id -u)" -o pid= | xargs -I{} cat /proc/{}/environ 2>/dev/null | tr '\0' '\n' | grep -m1 '^DISPLAY=' | cut --delimiter== -f2)
fi

if [[ -z $DISPLAY ]]
then
    echo "Use default display" | tee -a /opt/assistant/log/daemon.log
    DISPLAY=:0
fi

if [[ -z $XAUTHORITY ]]
then
    PATH_AUTH=$(find /var/run/gdm/ -name "auth-for-g*")
    if !( [ -z $PATH_AUTH ] )
    then
        XAUTHORITY=$PATH_AUTH/database
    fi
fi

if [[ -z $XAUTHORITY ]]
then
    PATH_AUTH=$(find /var/run/sddm/ -name "*" -type f)
    if !( [ -z $PATH_AUTH ] )
    then
        XAUTHORITY=$PATH_AUTH
    fi
fi

if [[ -z $XAUTHORITY ]]
then
    echo "Finding default dm xauthority" | tee -a /opt/assistant/log/daemon.log
    XAUTHORITY=$(find /var/run/lightdm/root/ -name "*" -type f -printf "%Ts %p\n" | sort -n | tail -1 | sed -r -e 's/^[0-9]+ //')
fi

if [ -n "$XAUTHORITY" ]
then	 
    echo "Found xauthority $XAUTHORITY" | tee -a /opt/assistant/log/daemon.log
    echo "Found display $DISPLAY" | tee -a /opt/assistant/log/daemon.log
    export DISPLAY XAUTHORITY 
    exec /opt/assistant/bin/asts | tee -a /opt/assistant/log/daemon.log
else 
    echo "Xauthority not found " | tee -a /opt/assistant/log/daemon.log
    exit 1
fi 

exit 0