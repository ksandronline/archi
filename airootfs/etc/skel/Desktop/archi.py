#!/usr/bin/python
# -*- coding: utf-8 -*-
# DESCRIPTION = _("archi - script for install archlinux.")
DESCRIPTION = "archi.py - скриптовая программа установки archlinux."
CONTACT     = "ru@ksandr.online"
AUTOR       = "ksandr"
STATUS      = "pre.alfa"
VERSION     = 20211116
BUILD       = 1
HOME_URL    = "http://archi.ksandr.online"


# --- TODO ---

# GRUB - UEFI and fdisk for UEFI
# Проверка режима загрузки ls /sys/firmware/efi/efivars
# Создать интерфейс для указания логина и пароля, а также для пароля root (сделать 3 фрем в 3 колонку)
# Показать все настройки перед установкой
# Заблокироовать вторую вкладку на время процесса установки.
# Отобразить размеры дисков и разделов
# Для отображения сетевых интерфейсов создать фрейм и добавлять новые интерфейсы горизонатльно в колонки.
# Определять bluetooth если есть устанавливать группу bluetooth
# ?? Добавить локализацию ?? LANG = os.environ.get('LANG') print(LANG)
    # todo для версии 2: Пересоздать заново весь графический интерфейс. 

# -----------------
# --- Настройки ---
# -----------------
add_user    = "archi"
user_pass   = "archi"
root_pass   = "archi" # !!! !НЕ! ЗАБУДЬ ПОМЕНЯТЬ ПАРОЛЬ !!!

# Списки пакетов
base_sys    = ["base", "base-devel", "btrfs-progs", "vim", "wget"]
kernel      = ["linux-firmware", "intel-ucode", "amd-ucode", "grub", "os-prober"]
linux_std   = ["linux", "linux-headers"]
linux_lts   = ["linux-lts", "linux-lts-headers"]    
linux_zen   = ["linux-zen", "linux-zen-headers"]
xorg        = ["xorg-server", "lightdm", "lightdm-gtk-greeter", "xf86-video-amdgpu", "xf86-video-ati", "xf86-video-intel", "xf86-video-nouveau", "tigervnc"]
xfce4       = ["xfce4", "xfce4-clipman-plugin", "xfce4-pulseaudio-plugin", "xfce4-xkb-plugin", "xfce4-screenshooter", "xfce4-taskmanager", \
    "ristretto", "arc-icon-theme", "arc-gtk-theme", "xdg-utils", "gvfs", "nfs-utils", "ntfs-3g", "sshfs", "unrar", "unzip", \
    "file-roller", "accountsservice", "tilda", "gnome-disk-utility"]
utils       = ["openssh", "avahi", "nss-mdns", "python-dbus", "sudo", "git", "mc", "cups", "samba", "zsh", "zsh-completions", "grc", "mpg123", "keepassxc", "mpv", \
    "perl-locale-gettext", "pulseaudio", "pulseaudio-zeroconf", "pavucontrol"]
pamac_aur   = ["pamac-aur"]
utils_aur   = ["pamac-zsh-completions", "yandex-disk-indicator", "man-pages-ru"]
fonts       = ["ttf-paratype", "otf-russkopis", "ttf-croscore", "ttf-dejavu", "ttf-ubuntu-font-family", "ttf-inconsolata", "ttf-liberation", "ttf-droid"]
brows       = ["firefox", "chromium", "yandex-browser-beta", "brave-bin", "discord", "transmission-cli", "transmission-gtk", "adguardhome-bin"]
custom      = ["rpi-imager", "conky-lua", "nodejs", "npm"]

root_mount_path     = "/mnt"
chroot              = ["arch-chroot", root_mount_path]
fs_type             = "mkfs.btrfs"  # TODO по по умолчанию используеться btrfs
domain              = "local"

log_install = '/home/archi/Desktop/install.log'
createlog = open(log_install, 'w')		# Создаём лог-файл
createlog.write("Готов.")
createlog.close()

# Installation_guide.html
gparted_guide_online    = "https://gparted.org/display-doc.php?name=help-manual&lang=ru"
install_guide_online    = "https://wiki.archlinux.org/title/Installation_guide_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)"
install_guide_local     = "/usr/share/doc/arch-wiki/html/ru/Installation_guide.html"
doc_local               = "/usr/share/doc/arch-wiki/html/ru/"

pacstrap = ["pacstrap"]
pacman = ["pacman", "-S", "--needed", "--noconfirm", "--config", "/root/pacman.conf"]
pamac = ["pamac", "install", "--no-confirm"]

color1 = '#f6f9fc'  # Archlinux.org
color2 = '#ecf2f5'
color3 = '#0088cc'
color4 = '#333333'
color5 = '#f6f9fc'

array_tz = {}
array_tz['MSK-01'] = ["Калининград", "Europe/Kaliningrad"]
array_tz['MSK+00'] = ["Москва Киров Волгоград", "Europe/Moscow"]
array_tz['MSK+01'] = ["Астрахань Самара Саратов Ульяновск", "Europe/Astrakhan"]
array_tz['MSK+02'] = ["Екатеринбург", "Asia/Yekaterinburg"]
array_tz['MSK+03'] = ["Омск", "Asia/Omsk"]
array_tz['MSK+04'] = ["Барнаул Новокузнецск Томск", "Asia/Barnaul"]
array_tz['MSK+05'] = ["Иркутск", "Asia/Irkutsk"]
array_tz['MSK+06'] = ["Якутск Хандыга Чита", "Asia/Yakutsk"]
array_tz['MSK+07'] = ["Владивосток", "Asia/Vladivostok"]
array_tz['MSK+08'] = ["Магадан Сахалин", "Asia/Magadan"]
array_tz['MSK+09'] = ["Анадырь Камчатка", "Asia/Anadyr"]
var_tz = list(array_tz)

# --------------------------------
#  --- Конфигурационные файлы ---
# --------------------------------

lightdm_conf = """
[LightDM]
run-directory=/run/lightdm

[Seat:*]
greeter-session=lightdm-gtk-greeter
allow-user-switching=true
session-wrapper=/etc/lightdm/Xsession

[XDMCPServer]
enabled=true
"""

lightdm_gtk_greeter_conf = """
[greeter]
theme-name = Adwaita-dark
icon-theme-name = Breeze_Obsidian
background = /usr/share/backgrounds/xfce/xfce-blue.jpg
position = 20%,center 50%,center
xft-antialias = true
xft-dpi = 96
xft-rgba = vrgb
xft-hintstyle = hintmedium
indicators = ~separator;~host;~spacer;~clock;~spacer;~session;~layout;~power;~separator
"""

xvnc_service = """
[Unit]
Description=XVNC Per-Connection Daemon

[Service]
ExecStart=-/usr/bin/Xvnc -inetd -query localhost -geometry 1920x1080 -once -SecurityTypes=None
User=nobody
StandardInput=socket
StandardError=syslog
"""

xvnc_socket = """
[Unit]
Description=XVNC Server

[Socket]
ListenStream=5900
Accept=yes

[Install]
WantedBy=sockets.target
"""

pamac_conf = """
RemoveUnrequiredDeps
RefreshPeriod = 6
NoUpdateHideIcon
SimpleInstall
EnableAUR
KeepBuiltPkgs
CheckAURUpdates
BuildDirectory = /var/tmp
KeepNumPackages = 2
MaxParallelDownloads = 4
"""

nsswitch_conf = """
passwd: files systemd
group: files [SUCCESS=merge] systemd
shadow: files
publickey: files
hosts: files mymachines myhostname mdns4_minimal [NOTFOUND=return] resolve [!UNAVAIL=return] dns
networks: files
protocols: files
services: files
ethers: files
rpc: files
netgroup: files
"""

avahi_vnc_service = """
<service-group>
  <name replace-wildcards="yes">%h</name> 
  <service>
    <type>_rfb._tcp</type>
    <port>5900</port>
  </service> 
</service-group>
"""

avahi_ssh_service = """
<service-group>
  <name replace-wildcards="yes">%h</name>
  <service>
    <type>_ssh._tcp</type>
    <port>22</port>
  </service>
</service-group>
"""

default_pa = """
load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24 auth-anonymous=1    # TODO Поменять IP на переменную
load-module module-zeroconf-publish
load-module module-zeroconf-discover
"""

# -----------------
# -----------------
# -----------------

import time
import os
import glob
import sys
import crypt
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from os.path import basename, dirname
from glob import glob

net_devs = {}
for dev in os.listdir("/sys/class/net/"):   # Спасибо https://stackoverflow.com/questions/3837069/how-to-get-network-interface-card-names-in-python
    if dev != 'lo':
        net_devs[dev] = {}

# --------------------------
#  --- Основные функции ---
# --------------------------

def install_arch():
    prepare_disk()                                  # Подготовка диска
    _run(pacstrap + [root_mount_path] + base_sys)    # Установка базовой системы
    basic_configure()                               # Конфигурирование базовой системы

    # Берём конфиг с iso для установки
    _run(["cp", "/etc/pacman.conf", root_mount_path + "/root/pacman.conf"])

    args = ["useradd", "--create-home", "--password", cryptPassword(user_pass,"md5"), add_user]    # Добавляем пользователя
    _run(chroot + args)
    args = ["usermod", "--password", cryptPassword(root_pass,"md5"), "root"]    # Меняем пароль для Root`а
    _run(chroot + args)
    fr_st_base_sys.configure(background=color3) # Первый пункт выполнен
    
    # Ядро
    if kernel_var.get() == 1:   linux = linux_std
    elif kernel_var.get() == 2: linux = linux_lts
    elif kernel_var.get() == 3: linux = linux_zen
    _run(chroot + pacman + kernel + linux)  # Установка ядра и загрузчика

    # Загрузчик
    grub_mkconfig = ["grub-mkconfig", "-o", "/boot/grub/grub.cfg"] 
    if grub_var.get() == 1:
        _run(chroot + grub_mkconfig)
        _run(chroot + ["grub-install", "/dev/"+use_disk.get()])  # BIOS
    elif grub_var.get() == 2:
        _run(chroot + grub_mkconfig)
        _run(chroot + ["grub-install"])  # UEFI
    elif grub_var.get() == 3:
        _show("Загрузчик не установлен.")
    fr_st_kernel.configure(background=color3)   # Второй пункт выполен

    # Установка дополнений:
    _run(chroot + pacman + xorg)

    _write([lightdm_conf],               root_mount_path + "/etc/lightdm/lightdm.conf")
    _write([lightdm_gtk_greeter_conf],   root_mount_path + "/etc/lightdm/lightdm-gtk-greeter.conf")

    _write([xvnc_service],   root_mount_path + "/etc/systemd/system/xvnc@.service")
    _write([xvnc_socket],    root_mount_path + "/etc/systemd/system/xvnc.socket")

    _run(chroot + ["systemctl", "enable", "lightdm.service"])
    fr_st_xorg.configure(background=color3)     # Третий пункт

    _run(chroot + pacman + xfce4)
    fr_st_xfce4.configure(background=color3)

    _run(chroot + pacman + utils)
    usermod = ["usermod", "--shell", "/bin/zsh", "root"]    # Меняем шелл для Root`а
    _run(chroot + usermod)
    usermod = ["usermod", "--shell", "/bin/zsh", add_user]    # Меняем шелл для юзера.
    _run(chroot + usermod)
    _write([add_user, "ALL=(ALL)", "ALL"], root_mount_path + "/etc/sudoers")  # Разрешаем юзеру sudo

    _write([nsswitch_conf], root_mount_path + "/etc/nsswitch.conf")      # Настраиваем Avahi
    _write([avahi_vnc_service], root_mount_path + "/etc/avahi/services/vnc.service")
    _write([avahi_ssh_service], root_mount_path + "/etc/avahi/services/ssh.service")
    _run(chroot + ["systemctl", "enable", "avahi-daemon.service"])
    _run(chroot + ["systemctl", "enable", "xvnc.socket"])

    _run(chroot + ["systemctl", "enable", "sshd.service"])       # Запускаем SSH сервер

    _write_end([default_pa], root_mount_path + "/etc/pulse/default.pa")      # Настраиваем звук по сети.
    fr_st_utils.configure(background=color3)

    # install_pamac()   # Функиця не работает с iso. Требуеться много заивсимостей. Работает на установленной системе.
    _run(chroot + pacman + pamac_aur)   # Поэтому ставим из пакета. см. /root/pacman.conf - подключен репозиторий archi.
    _write([pamac_conf],root_mount_path + "/etc/pamac.conf")
    fr_st_pamac.configure(background=color3)

    _run(chroot + pamac + utils_aur)
    fr_st_utils_aur.configure(background=color3)

    _run(chroot + pamac + fonts)
    fr_st_fonts.configure(background=color3)

    _run(chroot + pamac + brows)
    fr_st_brows.configure(background=color3)

    _run(chroot + pamac + custom)
    fr_st_custom.configure(background=color3)
    _run(["cp", log_install, root_mount_path + "/root/install.log"])
    _show("Установка Arch linux завершена.")
    _show("Лог-файл установки скопирован в /root/install.log")

def prepare_disk():
    # Если BIOS: отступаем 1 Мб от начала диска, создаём swap = ОЗУ, на всём оставшемся создаём раздел для корневой системы.
    # Если UEFI: создаём FAT раздел на 512 Мб, создаём swap = ОЗУ, на всём оставшемся создаём раздел для корневой системы.
    if use_disk_or_partition.get() == 1:    # Использовать весь диск
        if use_disk.get():
            parted = ["parted", "--script", "/dev/"+use_disk.get()]
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')    # Спасибо https://stackoverflow.com/questions/22102999/get-total-physical-memory-in-python
            mem_gib = mem_bytes/(1024.**3)
            mem_str = str(round(mem_gib))
            if grub_var.get() == 1:         # BIOS
                _run(parted + ["mklabel", "msdos"])
                _run(parted + ["mkpart", "primary", "linux-swap", "1MiB", mem_str+"GiB"])
                _run(parted + ["mkpart", "primary", "btrfs", mem_str+"GiB", "100%"])

                _run(["mkswap", "/dev/"+use_disk.get()+"1"])
                mkfs_command = ["mkfs.btrfs", "-f"]
                root_partition = ["/dev/"+use_disk.get()+"2"]
                _run(mkfs_command + root_partition)

                _run(["swapon", "/dev/"+use_disk.get()+"1"])
                _run(["mount", "/dev/"+use_disk.get()+"2", root_mount_path])
            elif grub_var.get() == 2:       # UEFI
                _run(parted + ["mklabel", "gpt"])
                _run(parted + ["mkpart", "primary", "fat32", "1MiB", "512MiB"])
                _run(parted + ["name", "1", "EFI"])
                _run(parted + ["set", "1", "esp", "on"])
                _run(parted + ["set", "1", "boot", "on"])
                _run(parted + ["mkpart", "primary", "linux-swap", "512MiB", mem_str+"GiB"])  # TODO Добавить к swap "512MiB"
                _run(parted + ["mkpart", "primary", "btrfs", mem_str+"GiB", "100%"])

                mkfs_command = ["mkfs.fat", "-F", "32"]
                uefi_partition = ["/dev/"+use_disk.get()+"1"]
                _run(mkfs_command + uefi_partition)
                uefi_mount = ["mount", "/dev/"+use_disk.get()+"1", root_mount_path+"/boot/efi"]
                _run(uefi_mount)

                _run(["mkswap", "/dev/"+use_disk.get()+"2"])
                mkfs_command = ["mkfs.btrfs", "-f"]
                root_partition = ["/dev/"+use_disk.get()+"3"]
                _run(mkfs_command + root_partition)

                _run(["swapon", "/dev/"+use_disk.get()+"2"])
                _run(["mount", "/dev/"+use_disk.get()+"3", root_mount_path])
            elif grub_var.get() == 3:       # None
                _run(parted + ["mklabel", "msdos"])
                _run(parted + ["mkpart", "primary", "linux-swap", "1MiB", mem_str+"GiB"])
                _run(parted + ["mkpart", "primary", "btrfs", mem_str+"GiB", "100%"])

                _run(["mkswap", "/dev/"+use_disk.get()+"1"])
                mkfs_command = ["mkfs.btrfs", "-f"]
                root_partition = ["/dev/"+use_disk.get()+"2"]
                _run(mkfs_command + root_partition)

                _run(["swapon", "/dev/"+use_disk.get()+"1"])
                _run(["mount", "/dev/"+use_disk.get()+"2", root_mount_path])     
        else:
            _show("Необходимо выбрать диск.")
    elif use_disk_or_partition.get() == 2:  # Использовать выбранный раздел.
        if select_partition.get():
            mkfs_command = ["mkfs.btrfs", "-f", select_partition.get()]
            _run(["mkfs.btrfs", "-f", select_partition.get()])
            _run(["mount", select_partition.get(), root_mount_path])
        else:
            _show("Необходимо выбрать раздел.")

def basic_configure():
    # fstab   
    _show("Генерируем файл /etc/fstab")
    genfstab_command = ["genfstab", "-U", root_mount_path]
    _run(genfstab_command)
    fstab = root_mount_path + "/etc/fstab"
    with open(fstab, "w") as file:
        Popen(genfstab_command, stdout=file, encoding='utf-8', text=True)

    # Locale
    locale_gen = """
ru_RU.UTF-8 UTF-8
en_US.UTF-8 UTF-8
    """
    _write([locale_gen],root_mount_path + "/etc/locale.gen")
    _run(chroot + ["locale-gen"])
    _write(["LANG=ru_RU.UTF-8"],root_mount_path + "/etc/locale.conf")
    vconsole_conf = """
KEYMAP=ru
FONT=cyr-sun16
    """
    _write([vconsole_conf],root_mount_path + "/etc/vconsole.conf")

    # Net
    hostname = entry_hostname.get()
    _show("Имя компьютера: "+ hostname +" -> /etc/hostname")
    _write([hostname],root_mount_path + "/etc/hostname")

    hosts = """
127.0.0.1   localhost
127.0.0.1   {hostname}.local {hostname}
    """.format(hostname=hostname)    # TODO Поменять ip
    _write([hosts],root_mount_path + "/etc/hosts")

    for dev in net_devs:        # Сетевые интерфейсы
        if net_devs[dev]["tk_var_DHCP"].get() == 1:
            wired_network = """# DHCP
[Match]
Name={dev}

[Network]
DHCP=yes
            """.format(dev=dev)
            _write([wired_network],root_mount_path + "/etc/systemd/network/20-wired.network")
        else:
            wired_network = """# Статический ip-адрес
[Match]
Name={dev}

[Network]
Address={ip}
Gateway={gw}
DNS={dns}
            """.format(dev=dev, ip=net_devs[dev]["ent_ip"].get(), gw=net_devs[dev]["ent_gw"].get(), dns=net_devs[dev]["ent_dns"].get())
            _write([wired_network],root_mount_path + "/etc/systemd/network/20-wired.network")
            
    _run(chroot + ["systemctl", "enable", "systemd-networkd"])
    _run(chroot + ["systemctl", "enable", "systemd-resolved"])

    _write(["domain="+domain],root_mount_path + "/etc/resolv.conf")

    # Time
    _run(chroot + ["ln", "-sf", "/usr/share/zoneinfo/"+ array_tz[combo_tz.get()][1], "/etc/localtime"])
    _run(chroot + ["hwclock", "--systohc"])
    _show("Часовой пояс: "+ combo_tz.get()+ " "+ array_tz[combo_tz.get()][0])

# TODO Сборку и установку pamac нужно перенести в chroot новой системы.
def install_pamac():        # Спасибо https://stackoverflow.com/questions/52693107/python-script-for-installing-aur-packages
    # args = ["pacman", "-S", "--noconfirm", "--needed"]
    pamac_deps = ["dbus-glib", "desktop-file-utils", "git", "json-glib", "libhandy", "libnotify", "libsoup", "polkit", "vte3", "appstream-glib", \
        "glib2", "gnutls", "asciidoc", "gettext", "gobject-introspection", "itstool", "libappindicator-gtk3", "meson", "ninja", "xorgproto", \
        "vala", "gtk3"]
    _run(chroot + pacman + ["--needed"] + pamac_deps)

    clone_and_makepkg(package_name="archlinux-appstream-data-pamac")
    clone_and_makepkg(package_name="libpamac-aur")
    clone_and_makepkg(package_name="pamac-aur")
    _write([pamac_conf],root_mount_path + "/etc/pamac.conf")

def clone_and_makepkg(package_name, aur_folder_path="/tmp/build/", uid=1000, gid=1000):
    git_url = "https://aur.archlinux.org/" + package_name + ".git"
    new_package_path = os.path.join(root_mount_path, aur_folder_path, package_name)

    if not os.path.exists(root_mount_path + aur_folder_path):
        os.mkdir(root_mount_path + aur_folder_path)
        os.chmod(root_mount_path + aur_folder_path, 0o777)

    _show("Загрузка " + git_url + " в " + new_package_path)
    # line = "Загрузка " + git_url + " в " + new_package_path 
    # txt_edit.insert(tk.END, line)
    with open(log_install, "a") as flog:
        Popen(["git", "clone", git_url, new_package_path], preexec_fn=demote(uid, gid), stdout=flog, stderr=STDOUT, encoding='utf-8', text=True).wait()
        # os.chdir(new_package_path)
        Popen(chroot + ["cd", aur_folder_path + package_name,  ";makepkg"], preexec_fn=demote(uid, gid), stdout=flog, stderr=STDOUT, encoding='utf-8', text=True).wait()

    built_packages = glob(new_package_path + os.sep + "*.pkg.tar.zst")
    for package in built_packages:
        _show("Установка пакета {}".format(package))

    # args = ["pacman", "-U", "--noconfirm", "--root", root_mount_path, "--dbpath", root_mount_path+"/var/lib/pacman"]
    # _run(args + built_packages)
    _run(chroot + pacman + built_packages)

def install_pamac_old():        # Спасибо https://stackoverflow.com/questions/52693107/python-script-for-installing-aur-packages
    # args = ["pacman", "-S", "--noconfirm", "--needed"]
    pamac_deps = ["dbus-glib", "desktop-file-utils", "git", "json-glib", "libhandy", "libnotify", "libsoup", "polkit", "vte3", "appstream-glib", \
        "glib2", "gnutls", "asciidoc", "gettext", "gobject-introspection", "itstool", "libappindicator-gtk3", "meson", "ninja", "xorgproto", \
        "vala", "gtk3"]
    _run(chroot + pacman + ["--needed"] + pamac_deps)

    clone_and_makepkg(package_name="archlinux-appstream-data-pamac")
    clone_and_makepkg(package_name="libpamac-aur")
    clone_and_makepkg(package_name="pamac-aur")
    _write([pamac_conf],root_mount_path + "/etc/pamac.conf")

def clone_and_makepkg_old(package_name, aur_folder_path="/tmp/build/", uid=1000, gid=1000):
    git_url = "https://aur.archlinux.org/" + package_name + ".git"
    new_package_path = os.path.join(aur_folder_path, package_name)

    if not os.path.exists(aur_folder_path):
        os.mkdir(aur_folder_path)
        os.chmod(aur_folder_path, 0o777)

    line = "Загрузка " + git_url + " в " + new_package_path 
    txt_edit.insert(tk.END, line)
    with open(log_install, "a") as flog:
        Popen(["git", "clone", git_url, new_package_path], preexec_fn=demote(uid, gid), stdout=flog, stderr=STDOUT, encoding='utf-8', text=True).wait()
        os.chdir(new_package_path)
        Popen("makepkg", preexec_fn=demote(uid, gid), stdout=flog, stderr=STDOUT, encoding='utf-8', text=True).wait()

    built_packages = glob(new_package_path + os.sep + "*.pkg.tar.zst")
    for package in built_packages:
        _show("Установка пакета {}".format(package))

    args = ["pacman", "-U", "--noconfirm", "--root", root_mount_path, "--dbpath", root_mount_path+"/var/lib/pacman"]
    _run(args + built_packages)

def demote(user_uid, user_gid):
    def apply_demotion():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return apply_demotion

def _run(exec_command):      # Выполняем команду с аргументами
    with open(log_install, "a") as flog:
        Popen(exec_command, stdout=flog, stderr=STDOUT, encoding='utf-8', text=True)

def _show(line):             # Печатаем строку в интерфейс программы
    txt_edit.insert(tk.END, _(line)+"\n")

def _write(text, outfile="/tmp/archi"):   # Пишем в файл: сначала файла перезаписывая то что там было
    with open(outfile, "w") as file:
        Popen(["echo"]+ text, stdout=file, encoding='utf-8', text=True)
    _show("В файл "+ outfile +" записываем:\n" + text[0])

def _write_end(text, outfile="/tmp/archi"):   # Пишем в файл: дописываем в конец файла
    with open(outfile, "a") as file:
        Popen(["echo"]+ text, stdout=file, encoding='utf-8', text=True)
    _show("В файл "+ outfile +" записываем:\n" + text[0])

def cryptPassword(password, algo=None):         # Спасибо https://programtalk.com/python-examples/crypt.METHOD_MD5/
    salts = {'md5': crypt.METHOD_MD5,
             'sha256': crypt.METHOD_SHA256,
             'sha512': crypt.METHOD_SHA512}
 
    if algo not in salts:
        algo = 'md5'
 
    cryptpw = crypt.crypt(password, salts[algo])
    return cryptpw

def fdisk(sdx,par):    # Спасибо https://stackoverflow.com/questions/163542/how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument
    p = Popen(['fdisk', sdx], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
    b = bytes(par, encoding='utf-8')
    fdisk_stdout = p.communicate(input=b)[0]
    with open(log_install, "a") as flog:
        flog.write(fdisk_stdout.decode())

def physical_drives():
    drive_glob = '/sys/block/*/device'
    return [basename(dirname(d)) for d in glob(drive_glob)]

def partitions(disk):
    partition_glob = '/sys/block/{0}/*/start'.format(disk)
    return [basename(dirname(p)) for p in glob(partition_glob)]

def disk():                     # Спасибо https://codereview.stackexchange.com/questions/152486/parsing-the-lsblk-output
    # fdisk -s /dev/sda2        # Спасибо https://www.tecmint.com/fdisk-commands-to-manage-linux-disk-partitions/
    disk = {}
    for d in physical_drives():
        disk[d] = partitions(d)
    return disk   

def custom_command():
    _show(DESCRIPTION)

def run_install():      # Начало процесса установки.
    # thrd = Thread(target=custom_command, daemon=True)
    # thrd = Thread(target=install_pamac, daemon=True)
    thrd = Thread(target=install_arch, daemon=True)
    thrd.start()


# ---------------------
#  --- Локализации ---
# ---------------------
# TODO
l18n = {}
l18n["ru_RU.UTF-8"] = {}
l18n["ru_RU.UTF-8"]["archi - script for install archlinux."] = "archi - скриптовая программа установки archlinux."
l18n["ru_RU.UTF-8"]["Hello world!"] = "Привет мир!"
l18n["ru_RU.UTF-8"]["Exit"] = "Выход"

def _(s):
    try:
        l18n[os.environ.get('LANG')][s]
        return l18n[os.environ.get('LANG')][s]
    except KeyError:
        return s
# DESCRIPTION = _("archi - script for install archlinux.")
# -------------------------------
#  --- Графический интерфейс ---
# -------------------------------

def tick():
    clock.after(200, tick)
    clock['text'] = time.strftime('%H:%M:%S')

def read_flog():        # Читаем лог файл и выводим его содержимое в текстовый фрейм
    for line in pop.stdout:
        txt_edit.insert(tk.END, line)

def upd_tz_label(event):
    var_lbl_tz.set(array_tz[combo_tz.get()][0])

def hide_partitions():
    for d in disk():
        fr_partitions[d].grid_forget()

def show_partitions():
    row = 0
    for d in all_disk.keys():
        rd_use_disc[d].grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
        row += 1
        fr_partitions[d].grid(row=row, column=1, sticky="nsew", padx=3, pady=3)
        row += 1
        for p in all_disk[d]:
            rd_select_partition[p].grid(column=0, sticky="nsew", padx=1, pady=1)
            row += 1

def gparted():
    _run(["gparted"])

def guide_online():
    Popen(["firefox", install_guide_online], encoding='utf-8', text=True)
    
def guide_local():
    Popen(["thunar", doc_local], encoding='utf-8', text=True)

def guide_gparted():
    Popen(["firefox", gparted_guide_online], encoding='utf-8', text=True)

# Спасибо https://python-scripts.com/tkinter
# Окно и его свойства
window = tk.Tk()
window.title("Установка Arch-linux русская версия.")
window.overrideredirect(False)      # Скрыть кнопки управления окном.
 
# window.rowconfigure(0, minsize=1300, weight=1)
# window.columnconfigure(1, minsize=1300, weight=1)

window.configure(background=color2)

var_lbl_tz = tk.StringVar()
var_lbl_tz.set("Москва")
var_interface = tk.StringVar()
var_welcome = tk.StringVar()
# var_welcome.set("Программа установки Arch linux на ваш компьютер.")
var_welcome.set(DESCRIPTION)
var_desc_1 = tk.StringVar()
var_desc_1.set("Процесс установки: ")
var_home_url = tk.StringVar()
var_home_url.set("Сайт проекта archi - " + HOME_URL)

use_disk_or_partition = IntVar()
use_disk_or_partition.set(1)
kernel_var = IntVar()
kernel_var.set(3)
grub_var = IntVar()
grub_var.set(1)

use_disk = StringVar()
use_disk.set("")
select_partition = StringVar()
select_partition.set("")

ttk.Style().configure("TButton", padding=6, relief=tk.GROOVE, font=("PT Serif Expert", "12"))
ttk.Style().configure("TLabel", padding=6, background=color2, foreground=color4, font=("PT Serif Expert", "12"))
ttk.Style().configure("TFrame", padding=6, background=color2, foreground=color4, font=("PT Serif Expert", "12"))
ttk.Style().configure("TLabelFrame", padding=6, background=color2, foreground=color4, font=("PT Serif Expert", "12"))
ttk.Style().configure("TRadiobutton", padding=6, background=color2, foreground=color4, font=("PT Serif Expert", "12"))
ttk.Style().configure("TNotebook", padding=6, background=color2, foreground=color4, font=("PT Serif Expert", "12"))

# Вкладки
page = ttk.Notebook(window)
welc_page = ttk.Frame(page)
sett_page = ttk.Frame(page)
inst_page = ttk.Frame(page)
page.add(welc_page, text='О программе', sticky="nsew")
page.add(sett_page, text='Параметры', sticky="nsew")
page.add(inst_page, text='Установка', sticky="nsew")
page.pack()
# page.pack(expand=1, fill='both')

# Фреймы
# 1
fr_welcome = tk.Frame(welc_page, bg=color2)
# 2
fr_setting = tk.Frame(sett_page, bg=color2)
fr_setting_right = tk.Frame(sett_page, bg=color2)
# 3
txt_edit = tk.Text(inst_page, bg=color1, fg=color4, font=("PT Serif Expert", "12"))
fr_buttons = tk.Frame(inst_page, bg=color2, borderwidth=4, padx=7, pady=7)

# Размещение фреймов
# 1
fr_welcome.grid(row=0, column=0, sticky="nsew")
# 2
fr_setting.grid(row=0, column=0, sticky="nsew")
fr_setting_right.grid(row=0, column=1, sticky="nsew")
# 3
txt_edit.grid(row=0, column=1, sticky="nsew")
fr_buttons.grid(row=0, column=0, sticky="ns")

# Скролбар
scr = Scrollbar(inst_page, command=txt_edit.yview)
txt_edit.configure(yscrollcommand=scr.set)
scr.grid(row=0, column=2, sticky="ns")

txt_edit.yview(END)

# Создание элементов

# 1-я вкладка информационная
lbl_welcome = tk.Label(fr_welcome, textvariable=var_welcome, bg=color2, fg=color4, font = ("PT Serif Expert", "16", "bold"))
lbl_desc_1 = tk.Label(fr_welcome, textvariable=var_desc_1, bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
btn_guide_online = ttk.Button(fr_welcome, text="Документация онлайн", command=guide_online)
btn_guide_local = ttk.Button(fr_welcome, text="Локальная копия", command=guide_local)
btn_guide_gparted = ttk.Button(fr_welcome, text="Документация по разбиению диска", command=guide_gparted)

lbl_home_url = tk.Label(fr_welcome, textvariable=var_home_url, bg=color2, fg=color4, font = ("PT Serif Expert", "12"))


# 1-я владка размещение элементов
lbl_welcome.grid    (row=0, column=0, sticky="ew", padx=1, pady=1)
lbl_desc_1.grid    (row=1, column=0, sticky="w", padx=1, pady=1)
btn_guide_online.grid    (row=2, column=0, sticky="w", padx=1, pady=1)
btn_guide_local.grid    (row=2, column=0, sticky="e", padx=1, pady=1)
btn_guide_gparted.grid    (row=3, column=0, sticky="w", padx=1, pady=1)

lbl_home_url.grid    (row=5, column=0, sticky="w", padx=1, pady=1)

# 2-я владка Настройки
fr_filesys = tk.LabelFrame(fr_setting, text='Файловая система', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
rb_filesys_use_disk = Radiobutton(fr_filesys, text='Использовать весь диск', variable=use_disk_or_partition, value=1, command=hide_partitions)
rb_filesys_choise_partition = Radiobutton(fr_filesys, text='Указать раздел для /', variable=use_disk_or_partition, value=2, command=show_partitions)
btn_gparted         = ttk.Button(fr_filesys, text="Редактировать разделы", command=gparted)

fr_kernel = tk.LabelFrame(fr_setting, text='Ядро', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
rb_kernel_std = Radiobutton(fr_kernel, text='Стандарное', variable=kernel_var, value=1)
rb_kernel_lts = Radiobutton(fr_kernel, text='LTS', variable=kernel_var, value=2)
rb_kernel_rlt = Radiobutton(fr_kernel, text='ZEN', variable=kernel_var, value=3)

fr_bios = tk.LabelFrame(fr_setting, text='Тип загрузчика GRUB', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
rb_grub_bios = Radiobutton(fr_bios, text='BIOS', variable=grub_var, value=1)
rb_grub_uefi = Radiobutton(fr_bios, text='UEFI', variable=grub_var, value=2)
rb_grub_none = Radiobutton(fr_bios, text='None', variable=grub_var, value=3)

fr_tz = tk.LabelFrame(fr_setting, text='Часовой пояс', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
combo_tz = ttk.Combobox(fr_tz, values=var_tz)
combo_tz.set("MSK+00")
combo_tz.bind("<<ComboboxSelected>>", upd_tz_label)
lbl_city = tk.Label(fr_tz, textvariable=var_lbl_tz, bg=color2, fg=color4, font = ("PT Serif Expert", "12"))

fr_net = tk.LabelFrame(fr_setting, text='Сеть', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
lbl_hostname = tk.Label(fr_net, text="Имя компьютера: ", bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
entry_hostname = tk.Entry(fr_net)
entry_hostname.insert(0, "archi")
# sep_net = ttk.Separator(fr_net, orient='horizontal')

fr_net_dev = tk.LabelFrame(fr_setting, text="Сетевые интерфейсы", bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
for dev in net_devs:
    var_interface.set(dev+ " : ")
    net_devs[dev]["tk_var_DHCP"] = IntVar()
    net_devs[dev]["tk_var_DHCP"].set(1)
    net_devs[dev]["lbl_net"] = tk.Label(fr_net_dev, textvariable=var_interface, bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
    net_devs[dev]["rb_net_dhcp"] = Radiobutton(fr_net_dev, variable=net_devs[dev]["tk_var_DHCP"], value=1, text="DHCP")
    net_devs[dev]["rb_net_stat"] = Radiobutton(fr_net_dev, variable=net_devs[dev]["tk_var_DHCP"], value=0, text="Статический адрес")
    net_devs[dev]["lbl_ip"] = tk.Label(fr_net_dev, text="ip/mask: ", bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
    net_devs[dev]["ent_ip"] = tk.Entry(fr_net_dev)
    net_devs[dev]["lbl_gw"] = tk.Label(fr_net_dev, text="Шлюз: ", bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
    net_devs[dev]["ent_gw"] = tk.Entry(fr_net_dev)
    net_devs[dev]["lbl_dns"] = tk.Label(fr_net_dev, text="dns: ", bg=color2, fg=color4, font = ("PT Serif Expert", "12"))
    net_devs[dev]["ent_dns"] = tk.Entry(fr_net_dev)

fr_use_disk = tk.LabelFrame(fr_setting_right, text='Выберите диск для установки', bg=color2, fg=color4, font = ("PT Serif Expert", "12"))

fr_partitions = {}
for d in disk():
    fr_partitions[d] = tk.Frame(fr_use_disk, bg=color2)

rd_use_disc = {}
rd_select_partition = {}
all_disk = disk()
for d in disk():
    rd_use_disc[d] = ttk.Radiobutton(fr_use_disk, variable=use_disk, value=d, text=d)
    for p in all_disk[d]:
        rd_select_partition[p] = Radiobutton(fr_partitions[d], variable=select_partition, value=p, text="/dev/"+p)

# 2-я владка размещение элементов
fr_filesys.grid(row=0, column=0, sticky="ew", padx=3, pady=3)
rb_filesys_use_disk.grid    (row=0, column=0, sticky="ew", padx=1, pady=1)
rb_filesys_choise_partition.grid    (row=1, column=0, sticky="ew", padx=1, pady=1)
btn_gparted.grid    (row=3, column=0, sticky="ew", padx=1, pady=1)

fr_kernel.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
rb_kernel_std.grid    (row=0, column=0, sticky="nsew", padx=1, pady=1)
rb_kernel_lts.grid    (row=0, column=1, sticky="nsew", padx=1, pady=1)
rb_kernel_rlt.grid    (row=0, column=2, sticky="nsew", padx=1, pady=1)

fr_bios.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)
rb_grub_bios.grid    (row=0, column=0, sticky="nsew", padx=1, pady=1)
rb_grub_uefi.grid    (row=0, column=1, sticky="nsew", padx=1, pady=1)
rb_grub_none.grid    (row=0, column=2, sticky="nsew", padx=1, pady=1)

fr_tz.grid(row=3, column=0, sticky="ew", padx=3, pady=3)
combo_tz.grid    (row=0, column=0, sticky="n", padx=1, pady=1)
lbl_city.grid    (row=0, column=1, sticky="nsew", padx=1, pady=1)

fr_net.grid(row=4, column=0, sticky="ew", padx=3, pady=3)
lbl_hostname.grid    (row=0, column=0, sticky="e", padx=1, pady=1)
entry_hostname.grid    (row=0, column=1, sticky="w ", padx=1, pady=1)
# sep_net.grid    (row=1, column=0, sticky="nsew", padx=1, pady=1)

fr_net_dev.grid    (row=5, column=0, sticky="nsew", padx=3, pady=3)

for i,dev in enumerate(net_devs):
    net_devs[dev]["lbl_net"].grid    (row=0 + i, column=0, sticky="w", padx=1, pady=1)
    net_devs[dev]["rb_net_dhcp"].grid    (row=0 + i, column=1, sticky="e", padx=1, pady=1)
    net_devs[dev]["rb_net_stat"].grid    (row=0 + i, column=2, sticky="e", padx=1, pady=1)
    net_devs[dev]["lbl_ip"].grid    (row=1 + i, column=1, sticky="e", padx=1, pady=1)
    net_devs[dev]["ent_ip"].grid    (row=1 + i, column=2, sticky="w", padx=1, pady=1)
    net_devs[dev]["lbl_gw"].grid    (row=2 + i, column=1, sticky="e", padx=1, pady=1)
    net_devs[dev]["ent_gw"].grid    (row=2 + i, column=2, sticky="w", padx=1, pady=1)
    net_devs[dev]["lbl_dns"].grid    (row=3 + i, column=1, sticky="e", padx=1, pady=1)
    net_devs[dev]["ent_dns"].grid    (row=3 + i, column=2, sticky="w", padx=1, pady=1)

fr_use_disk.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)

row = 0
for d in all_disk.keys():
    rd_use_disc[d].grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
    row += 1        

# 3-я вкладка Установка
clock           = tk.Label(fr_buttons, font = ("PT Serif Expert", "24"), bg=color2, fg=color3)
lbl_install     = tk.Label(fr_buttons, text="Установка",bg=color2, fg=color4, font = ("PT Serif Expert", "16", "bold underline"))
lbl_base_sys    = ttk.Label(fr_buttons, text="Основная система")
lbl_kernel      = ttk.Label(fr_buttons, text="Ядро и загрузчик")
lbl_xorg        = ttk.Label(fr_buttons, text="Xorg сервер")
lbl_xfce4       = ttk.Label(fr_buttons, text="Набор xfce4")
lbl_utils       = ttk.Label(fr_buttons, text="Утилиты")
lbl_pamac       = ttk.Label(fr_buttons, text="Установка pamac")
lbl_utils_aur   = ttk.Label(fr_buttons, text="Утилиты из AUR")
lbl_fonts       = ttk.Label(fr_buttons, text="Шрифты")
lbl_brows       = ttk.Label(fr_buttons, text="Браузеры")
lbl_custom      = ttk.Label(fr_buttons, text="Бонусы")
btn_install     = ttk.Button(fr_buttons, text="Установить", command=run_install)    # Кнопка начать установку.
btn_exit        = ttk.Button(fr_buttons, text=_("Exit"), command=exit)

# Статус выполнения
fr_st_base_sys  = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_kernel    = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_xorg      = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_xfce4     = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_utils     = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_pamac     = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_utils_aur = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_fonts     = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_brows     = tk.Frame(fr_buttons, width=12, height=12, bg="white")
fr_st_custom    = tk.Frame(fr_buttons, width=12, height=12, bg="white")

# 3-я вкладка размещение элементов
clock.grid          (row=0, column=0, sticky="ew", padx=5, pady=5)
lbl_install.grid    (row=1, column=0, sticky="ew", padx=1, pady=1)
lbl_base_sys.grid   (row=2, column=0, sticky="w", padx=7, pady=0)
lbl_kernel.grid     (row=3, column=0, sticky="w", padx=7, pady=0)
lbl_xorg.grid       (row=4, column=0, sticky="w", padx=7, pady=0)
lbl_xfce4.grid      (row=5, column=0, sticky="w", padx=7, pady=0)
lbl_utils.grid      (row=6, column=0, sticky="w", padx=7, pady=0)
lbl_pamac.grid      (row=7, column=0, sticky="w", padx=7, pady=0)
lbl_utils_aur.grid  (row=8, column=0, sticky="w", padx=7, pady=0)
lbl_fonts.grid      (row=9, column=0, sticky="w", padx=7, pady=0)
lbl_brows.grid      (row=10, column=0, sticky="w", padx=7, pady=0)
lbl_custom.grid      (row=11, column=0, sticky="w", padx=7, pady=0)
btn_install.grid    (row=14, column=0, sticky="ew", padx=5, pady=5)
btn_exit.grid       (row=15, column=0, sticky="ew", padx=5)

fr_st_base_sys.grid (row=2, column=1, sticky="e", padx=0, pady=0)
fr_st_kernel.grid   (row=3, column=1, sticky="e", padx=0, pady=0)
fr_st_xorg.grid     (row=4, column=1, sticky="e", padx=0, pady=0) 
fr_st_xfce4.grid    (row=5, column=1, sticky="e", padx=0, pady=0)
fr_st_utils.grid    (row=6, column=1, sticky="e", padx=0, pady=0)
fr_st_pamac.grid    (row=7, column=1, sticky="e", padx=0, pady=0)
fr_st_utils_aur.grid(row=8, column=1, sticky="e", padx=0, pady=0) 
fr_st_fonts.grid    (row=9, column=1, sticky="e", padx=0, pady=0)
fr_st_brows.grid    (row=10, column=1, sticky="e", padx=0, pady=0)
fr_st_custom.grid   (row=11, column=1, sticky="e", padx=0, pady=0)

# Новый Thread для заполнения формы txt_edit
pop = Popen(["tail", "-f", log_install], stdout=PIPE, encoding='utf-8')
thrd_txt = Thread(target=read_flog, daemon=True)
thrd_txt.start()

clock.after_idle(tick) 
window.mainloop()

