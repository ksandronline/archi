## archi - профиль для archiso

Данный репозиторий содержит готовый профиль для сборки iso образа загрузочного диска Arch linux с пред настроенным русским языком.

![image](https://raw.githubusercontent.com/ksandronline/archi/main/screenshots/screen-1.png)

![image](https://raw.githubusercontent.com/ksandronline/archi/main/screenshots/screen-2.png)

![image](https://raw.githubusercontent.com/ksandronline/archi/main/screenshots/screen-3.png)

![image](https://raw.githubusercontent.com/ksandronline/archi/main/screenshots/screen-4.png)

Ниже приведён краткий список команд необходимых для создания своего live диска.

### 1. Скачиваем профиль

* а) Установить пакет archi используя [PKGBUILD](http://archi.ksandr.online/downloads/) файл.
Он запишет файлы в стандартный каталог профилей /usr/share/archiso/configs. Далее следуем документации по [Archiso](https://wiki.archlinux.org/title/Archiso_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)):

Копируем профиль

`# cp -r /usr/share/archiso/configs/archi/ archi`

* б) Можно просто скачать данный репозиторий, например так:

`git clone https://github.com/ksandronline/archi.git`

### 2. Редактируем профиль
Редактируем профиль по своему усмотрению.
Более подробное описание есть в [Wiki](https://github.com/ksandronline/archi/wiki)

### 3. Создаём образ

Пример команды:

`# mkarchiso -v -w /home/ksandr/work -o /home/ksandr/work /home/ksandr/archi`
> Примечание: "ksandr" надо заменить на имя вашего пользователя.

Файл iso-образа будет находиться в "/home/ksandr/work"

### Скачать готовый образ archi-202X.XX.XX-x86_64.iso:
[Страница загрузки](http://archi.ksandr.online/downloads/)

#### Особые дополнения включенные в образ

[AdGuard Home](https://github.com/AdguardTeam/AdguardKnowledgeBase/blob/master/10.home/01.overview/docs.ru.md) описание на странице разработчика.

[Ассистент](https://мойассистент.рф/%D0%BE_%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B5) описание на странице разработчика.

[archi.py](https://github.com/ksandronline/archi/wiki/archi) python-скрипт для установки Arch linux с графическим интерфейсом.
