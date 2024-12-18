# Используем официальный образ Python в качестве базового
   FROM python:3.12.6-slim

   # Устанавливаем рабочую директорию
   WORKDIR /ap

   # Копируем файлы проекта в контейнер
   COPY . .

   # Устанавливаем зависимости
   RUN pip install --no-cache-dir -r requirements.txt

   # Команда для запуска вашего бота
   CMD ["python", "main.py"]