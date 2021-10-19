#!/bin/bash
LOG_TO_FILE=/opt/assistant/log/daemon.log

echo " Start Assistant daemon setup script"

#
# get init system and os version
#

if [ -f /etc/os-release ]; then
    . /etc/os-release
fi

ID=$(echo "$ID" | sed -r 's/\"//g')
VER=$(echo "$VERSION_ID" | sed -r 's/\"//g')
VER_TEMP=$(echo "$VER" | sed -r 's/\..*//')
if [ -L /sbin/init ]
then
    SYS=$(readlink /sbin/init | sed -r 's/.*\///')
else
    SYS="init"
fi

if [[ $ID == "calculate" ]]
then
    SYS="openrc"
fi

echo "Found $SYS initialization system"

#
# check root sudo entry
#

SUDO_FILE="/etc/sudoers"
SUDO_PATTERN="root ALL=(ALL) /opt/assistant/bin/assistant"
SUDO_REGEXP_PATTERN="root ALL=(ALL) \/opt\/assistant\/bin\/assistant"

if grep -q "$SUDO_REGEXP_PATTERN" $SUDO_FILE
then 
    echo "Sudo main entry already exist" 
else
    echo "$SUDO_PATTERN" >> $SUDO_FILE
fi


#
# create service
#

case "${ID}" in
	"calculate"|"gentoo")
		echo "Calculate linux detected, run openRC setup"
		rc-update delete zassistantd
		eselect rc stop zassistantd
		cp /opt/assistant/scripts/openrc.s /etc/init.d/zassistantd
		cp /opt/assistant/scripts/openrc.t /opt/assistant/scripts/runasts.sh 
		cp /opt/assistant/scripts/ast_restart.t /opt/assistant/scripts/ast_restart.sh
                cp /opt/assistant/scripts/assistant.desktop /usr/share/applications/
		chmod +x /etc/init.d/zassistantd

		echo "Files copied"

		/sbin/rc-update add zassistantd default
		/sbin/rc-service zassistantd start

		echo "Service runned"

		#
		# create cron task
		#
		CRON_PATTERN="*/1 * * * * root /opt/assistant/scripts/ast_restart.sh"
		CRON_REGEXP_PATTERN="^\*\/1 \* \* \* \* root \/opt\/assistant\/scripts\/ast_restart\.sh$"
		CRON_FILE="/etc/crontab"

		if grep -q "$CRON_REGEXP_PATTERN" $CRON_FILE
		then 
		    echo "Crontab entry already exist" >> $LOG_TO_FILE
		    echo "Crontab entry already exist"
		else
		    echo "Adding crontab entry" >> $LOG_TO_FILE
		    echo "Adding crontab entry"
		    echo "$CRON_PATTERN" >> $CRON_FILE
		fi

		echo "Cron task created"

	;;
        *)
	  cp /opt/assistant/scripts/assistant.service /lib/systemd/system/assistant.service
	  systemctl enable assistant.service
	  systemctl start assistant.service
	;;
esac

exit 0
