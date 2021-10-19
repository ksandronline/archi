#!/bin/bash

echo "Настройка работы приложения"

d=$(dirname $0)

sh ${d}/cert.sh --install

if [[ $? != 0 ]]
then
    echo "Настройка приложения завершена с ошибкой"
    exit 1
fi

sh ${d}/inst_daemon.sh

echo "Настройка приложения завершена"
exit 0