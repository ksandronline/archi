#!/bin/bash
echo "############################################################"
echo "# Starting customize_airootfs.sh"
echo "############################################################"

# Error management of set command
echo "Set command error management"
set -e -u

# Locale settings
echo "Locale settings"
sed -i 's/#\(ru_RU\.UTF-8\)/\1/' /etc/locale.gen
locale-gen
echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "KEYMAP=ru" > /etc/vconsole.conf
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
cp -aT  /skel/ /home/archi/

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
" > '/home/archi/Desktop/Установка Arch Linux.desktop'

chown archi:users -R /home/archi
chmod 755 /home/archi
chmod +x -v /home/archi/Desktop/*.desktop

# Configure SSH
# sed -i 's/#\(PermitRootLogin \).\+/\1yes/' /etc/ssh/sshd_config

# Configure Pacman
# echo "pacman config"
# sed -i 's/#\[multilib]/\[multilib]/g' /etc/pacman.conf
# sed -i '/^#\[multilib]/{N;s/\n#/\n/}' /etc/pacman.conf
# sed -i "s/#Server/Server/g" /etc/pacman.d/mirrorlist

# Configure logging
# echo "Logging config"
# sed -i 's/#\(Storage=\)auto/\1volatile/' /etc/systemd/journald.conf

# Fix the hibernate function
# echo "Fixing hibernate function"
# sed -i 's/#\(HandleSuspendKey=\)suspend/\1ignore/' /etc/systemd/logind.conf
# sed -i 's/#\(HandleHibernateKey=\)hibernate/\1ignore/' /etc/systemd/logind.conf
# sed -i 's/#\(HandleLidSwitch=\)suspend/\1ignore/' /etc/systemd/logind.conf

chmod +x -v /var/lib/adguardhome/AdGuardHome
/var/lib/adguardhome/AdGuardHome -s install

chmod +x -Rv /opt/assistant/

chmod +x -Rv /root/Desktop/

# Services
echo "Systemd services"
systemctl enable NetworkManager.service
systemctl enable AdGuardHome.service

systemctl enable avahi-daemon.service
systemctl enable xvnc.socket

echo "############################################################"
echo "# customize_airootfs.sh Done"
echo "############################################################"
