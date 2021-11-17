#!/bin/bash
echo "####################################"
echo " # Starting customize_airootfs.sh #"
echo "####################################"

# Error management of set command
#echo "Set command error management"
set -e -u

echo "Настройка времени"
timedatectl set-ntp true
hwclock --systohc

echo "Настройка home root"
cp -aT  /etc/skel/ /root/
chmod 700 -v /root
chmod +x -v /root/Desktop/*.desktop
rm -v /root/Desktop/archi.py
ln -sfv /home/archi/Desktop/archi.py /root/Desktop/archi.py
ln -sfv /root/Downloads /root/Загрузки
ln -sfv /usr/share/doc/arch-wiki/html/ru "/root/Desktop/Оффициальное WiKi локальная версия"

echo "Настройка home archi"
ln -sfv /home/archi/Downloads /home/archi/Загрузки
ln -sfv /usr/share/doc/arch-wiki/html/ru "/home/archi/Desktop/Оффициальное WiKi локальная версия"

echo "################################"
echo " # customize_airootfs.sh Done #" 
echo "################################"
