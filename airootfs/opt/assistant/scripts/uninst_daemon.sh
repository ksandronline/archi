#!/bin/bash

echo " Start Assistant daemon setup script"

SUDO_FILE="/etc/sudoers"
SUDO_PATTERN="root ALL=(ALL) /opt/assistant/bin/assistant"
SUDO_REGEXP_PATTERN="root ALL=(ALL) \/opt\/assistant\/bin\/assistant"

    # remove old sudo task
    if grep -q "$SUDO_REGEXP_PATTERN" $SUDO_FILE
    then
        echo "Removing old sudo entry" 
        sed -i "/${SUDO_REGEXP_PATTERN}/d" $SUDO_FILE
    fi

CRON_PATTERN="*/1 * * * * root /opt/assistant/scripts/ast_restart.sh"
CRON_REGEXP_PATTERN="^\*\/1 \* \* \* \* root \/opt\/assistant\/scripts\/ast_restart\.sh$"
CRON_FILE="/etc/crontab"
    # remove old cron task
    if grep -q "$CRON_REGEXP_PATTERN" $CRON_FILE
    then
        echo "Removing old cron entry" 
        sed -i "/${CRON_REGEXP_PATTERN}/d" $CRON_FILE
    fi

# openRC
rc-update delete zassistantd
eselect rc stop zassistantd
killall assistant
killall asts

# systemd
systemctl stop assistant.service
systemctl disable  assistant.service

exit 0
