# Используем официальный образ Python в качестве базового образа
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы requirements.txt и install.sh в рабочую директорию
COPY requirements.txt requirements.txt
COPY install.sh install.sh

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Запускаем скрипт установки модели
RUN chmod +x install.sh
RUN ./install.sh

# Устанавливаем команду по умолчанию для запуска контейнера
CMD ["python", "main.py"]