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
ln -sfv /root/Downloads /root/Загрузки
ln -sfv /usr/share/doc/arch-wiki/html/ru "/root/Desktop/Оффициальное WiKi локальная версия"

echo "Настройка home archi"
cp -v /usr/share/applications/install.desktop /home/archi/Desktop/install.desktop
ln -sfv /home/archi/Downloads /home/archi/Загрузки
ln -sfv /usr/share/doc/arch-wiki/html/ru "/home/archi/Desktop/Оффициальное WiKi локальная версия"
chmod +x -v /home/archi/Desktop/*.desktop

echo """Приветствую.

Я создаю этот проект для удобства использования системы Arch linux.
Исходные файлы находятся в открытом доступе и доступны в репозитории.
Моей целью является создание завершённых образов дисков и простой
системы для их создания.

С уважением ксандр.""" > "/home/archi/Desktop/Обращение к пользователю.md"
echo "################################"
echo " # customize_airootfs.sh Done #" 
echo "################################"
