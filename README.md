# Веб-приложение для учёта складских запасов ресурсов
Приложение позволяет получать список ресурсов, добавлять новый, изменять и удалять существующие ресурсы (CRUD).

## Подготовка
    git clone https://github.com/ex10se/InventoryControl.git
    cd InventoryControl
## Разработка
Windows

    virtualenv -p python venv
    cd venv/Scripts
    activate.bat
Linux

    sudo apt install libpq-dev python3-dev build-essential virtualenv
    virtualenv -p python venv
    cd venv/bin
    source activate

    cd ../..
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser

    python manage.py runserver

