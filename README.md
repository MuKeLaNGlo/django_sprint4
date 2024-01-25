# django_sprint4
Проект делал во время обучения на площадке Яндекс Практикум

Этот репозиторий содержит проект Blogicum. Проект представляет собой простое приложение для ведения блога, которое позволяет пользователям создавать, редактировать и удалять сообщения в блоге.

## Установка
```sh
git clone https://github.com/MuKeLaNGlo/django_sprint4.git
```
Затем нужно установить зависимости в виртуальное окружение, выполнив следующие команды в каталоге проекта:
```sh
python -m venv venv
source .\venv\Scripts\activate
pip install -r requirements.txt
```
Обязательно примените миграции
```sh
python manage.py migrate
```
По желанию создайте пользователя
```sh
python3 manage.py runserver
```

Есть фикстуры, чтобы их можно применить нужно переместить файл ```db.json``` в папку ```blogicum``` и выполнить команду:
```sh
python manage.py loaddata dj.json
```
## Запуск проекта
Чтобы запустить проект, вы можете использовать следующую команду в каталоге проекта:
```sh
python manage.py runserver
```
Это запустит сервер разработки на порту 8000. После этого вы сможете получить доступ к проекту по адресу http://localhost:8000/.
