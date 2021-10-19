#!/bin/bash

#PATH_LOG="tee -a /opt/assistant/log/daemon.log"

LOG_TO_FILE="/opt/assistant/log/cert.log"

{
	echo "--------------------------------------------------------------------"
	date
} >> $LOG_TO_FILE
echo "Start Assistant cert script" >> $LOG_TO_FILE

if [ -f /etc/os-release ]; then
    . /etc/os-release
fi
ID=$(echo "$ID" | sed -r 's/\"//g')
VER=$(echo "$VERSION_ID" | sed -r 's/\"//g')
VER_TEMP=$(echo "$VER" | sed -r 's/\..*//')

mkdir -p /etc/assistant/cert/
CERT_PATH=/etc/assistant/cert/ca-cert-native

if [ -L /sbin/init ]
then
    SYS=$(readlink /sbin/init | sed -r 's/.*\///')
else
    SYS="init"
fi

remove_ca()
{
    rm -rf /etc/assistant
    if [[ $? == 0 ]]
    then
	return 0;
    else
	return 1
    fi
}

make_ca()
{
	case "${ID}" in
	"calculate")
	    if [[ -f /etc/ssl/certs/ca-certificates.crt ]]
		then
		    ln -s /etc/ssl/certs/ca-certificates.crt $CERT_PATH
		    return 0;
		fi
	;;
	"rosa")
	    if [[ $VER_TEMP == "2014" || $VER_TEMP == "2016" || $VER_TEMP == "2019" ]]
	    then
		if [[ -f /etc/pki/tls/certs/ca-bundle.crt ]]
		then
		    ln -s /etc/pki/tls/certs/ca-bundle.crt $CERT_PATH
		    return 0;
		fi
	    else
   		echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
		echo "Неподдерживаемая версия $ID - $VER"
	        return 1
    	    fi
	;;
        "astra")
	    #echo "VER_TEMP = $VER_TEMP VER = $VER"
	    if [[ $VER_TEMP == "1" || $VER_TEMP == "2" ]]
            then
        	if [[ -f /etc/ssl/certs/ca-certificates.crt ]]
		then
		    ln -s /etc/ssl/certs/ca-certificates.crt $CERT_PATH
		    return 0;
		fi
	    else
		echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
		echo "Неподдерживаемая версия $ID - $VER" 
		return 1
	    fi
	;;
        "altlinux")
    	CPENAME=$(echo "$CPE_NAME" | cut -d: -f4)
	    if [[ $VER_TEMP == "7" ]]
	    then
		if [[ -f /usr/share/ca-certificates/ca-bundle.crt ]]
		then
		    ln -s /usr/share/ca-certificates/ca-bundle.crt $CERT_PATH
		    return 0;
		fi
	    else
		if [[ $VER = "9.1" ]]
		then
		    if [[ -f /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem ]]
		    then
			ln -s /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem $CERT_PATH
			return 0;
		    fi
		else
		    if [[ $VER_TEMP == "8" || $VER_TEMP == "9" ]]
		#    if [[ $CPENAME != "kworkstation" ]]
		    then
			if [[ -f /etc/pki/tls/certs/ca-bundle.crt ]]
			then
			    ln -s /etc/pki/tls/certs/ca-bundle.crt $CERT_PATH
			    return 0;
			fi
		    else
			echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
			echo "Неподдерживаемая версия $ID - $VER"
			return 1
		    fi
		fi
	    fi
	;;
        "ubuntu")
	    if [[ $VER_TEMP == "16" || $VER_TEMP == "18" || $VER_TEMP == "19" || $VER_TEMP == "20" ]]
	    then
		if [[ -f /etc/ssl/certs/ca-certificates.crt ]]
		then
		    ln -s /etc/ssl/certs/ca-certificates.crt $CERT_PATH
		    return 0;
		fi
	    else
		echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
		echo "Неподдерживаемая версия $ID - $VER"
		return 1
	    fi
        ;;
        "centos")
        if [[ $VER_TEMP == "7" ]]
    	    then
		if [[ -f /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem ]]
		then
		    ln -s /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem $CERT_PATH
		    return 0;
		fi
	    else
   		echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
		echo "Неподдерживаемая версия $ID - $VER"
	        return 1
    	    fi
	;;
	"rels" | "redos")
    	    if [[ $VER_TEMP == "7" ]]
    	    then
    		if [[ -f /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem ]]
		then
		    ln -s /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem $CERT_PATH
		    return 0;
		fi
	    else
   		echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
		echo "Неподдерживаемая версия $ID - $VER"
	        return 1
    	    fi
	;;
	"goslinux")
	    if [[ -f /etc/pki/tls/certs/ca-bundle.crt ]]
	    then
	    ln -s /etc/pki/tls/certs/ca-bundle.crt $CERT_PATH
		return 0;
	    fi
	;;
        *)
   	    echo "Unsupported version $ID - $VER" >> $LOG_TO_FILE
	    echo "Неподдерживаемая версия $ID - $VER"
	    return 1
	;;
    esac
    return 2
}

if [[ $1 == --install ]]
then
    echo "Installing CA..." >> $LOG_TO_FILE
    echo "Установка CA..."
    make_ca
    MRUN=$?
	if [[ $MRUN == 0 ]]
	then
    	    echo "Installing CA done" >> $LOG_TO_FILE
            echo "Установка CA завершена"
	else
	    echo "Don't set path to CA" >> $LOG_TO_FILE
            echo "Путь к CA не установлен"
	fi
else
    if [[ $1 == --uninstall ]]
    then
        echo "Uninstalling CA daemon..." >> $LOG_TO_FILE
        echo "Удаление CA..." 
	remove_ca
	if [[ $? == 0 ]]
	then
            echo "Uninstalling CA done" >> $LOG_TO_FILE
	    echo "Удаление CA завершено"
	else
	    echo "Don't remove path to CA" >> $LOG_TO_FILE
            echo "Путь к CA удалить не возможно"
        fi
    else
    	echo "Invalid params" >> $LOG_TO_FILE
    	echo "Неверные параметры"
	exit 1
    fi
fi

echo "Assistant CA setup script complete" >> $LOG_TO_FILE
echo "" >> $LOG_TO_FILE

exit 0
