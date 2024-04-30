# Используйте образ Python 3.9
FROM python:3.9

# Установите переменную окружения для предотвращения вывода байт-кода в stdout
ENV PYTHONDONTWRITEBYTECODE 1
# Отключите буферизацию вывода, чтобы логи отображались в реальном времени
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию в /app
WORKDIR /app

# Создайте Docker volume для хранения данных базы данных, если используется SQLite3, раскомментируйте
# VOLUME /app/db_data

# Скопируйте зависимости проекта в контейнер
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Скопируйте все содержимое текущей директории в контейнер
COPY . /app/

# Создайте миграции и примените их, если используется SQLite3, раскомментируйте
# RUN python manage.py makemigrations && python manage.py migrate

# Создание суперпользователя, если используется SQLite3, раскомментируйте
# RUN python manage.py createsuperuser --username admin --email admin@example.com --noinput --password mypassword

# Соберите статические файлы Django, если используется SQLite3, раскомментируйте
# RUN python manage.py collectstatic --noinput

# Запустите сервер Django
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python mqtt_subscriber.py"]
