#!/bin/bash
echo "####################################"
echo " # Starting customize_airootfs.sh #"
echo "####################################"

# Error management of set command
echo "Set command error management"
set -e -u

# Locale settings
echo "Locale settings"
sed -i 's/#\(ru_RU\.UTF-8\)/\1/' /etc/locale.gen
locale-gen
echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "KEYMAP=ruwin_alt-UTF-8" > /etc/vconsole.conf 	# KEYMAP=ruwin_alt-UTF-8
echo "FONT=cyr-sun16" > /etc/vconsole.conf


# Timezone
echo "Timezone"
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
timedatectl set-ntp true
hwclock --systohc

# Hostname
echo "Hostname"
echo "archi" > /etc/hostname
# Root user settings

# Remove standart config zsh
rm /etc/zsh/zshrc

echo "Autologin"
groupadd -r autologin
gpasswd -a archi autologin

# Copy skel
echo "Copy skel"
cp -aT  /skel/ /etc/skel/

#usermod -s /usr/bin/zsh root
cp -aT  /skel/ /root/
chmod 700 -v /root

# Create user archi
echo "Create user archi"
# useradd --create-home --shell /bin/zsh archi
mkdir /home/archi
cp -aT /skel/ /home/archi/

ln -sf /home/archi/Downloads /home/archi/Загрузки

echo "[Desktop Entry]
Version=1.0
Type=Application
Name=Установка Arch Linux
Comment=Установка Arch Linux на этот компьютер.
Exec=/usr/bin/pkexec python /home/archi/Desktop/archi.py
Icon=archlinux-logo
Path=
Terminal=false
StartupNotify=false
" > '/home/archi/Desktop/install.desktop'

chown archi:users -R /home/archi
chmod 755 /home/archi
chmod +x -v /home/archi/Desktop/*.desktop

# chmod +x -v /var/lib/adguardhome/AdGuardHome
/var/lib/adguardhome/AdGuardHome -s install

# chmod +x -Rv /opt/assistant/

chmod +x -Rv /root/Desktop/

# Services
echo "Systemd services"
systemctl enable systemd-resolved.service
systemctl enable NetworkManager.service
systemctl enable AdGuardHome.service

systemctl enable avahi-daemon.service
systemctl enable xvnc.socket

echo "################################"
echo " # customize_airootfs.sh Done #" 
echo "################################"
