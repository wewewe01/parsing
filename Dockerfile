FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 lsb-release fonts-liberation \
    libnss3 libxss1 libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 xvfb \
    ca-certificates && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome через официальный репозиторий
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Установка Python-зависимостей
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Разрешаем запуск
RUN chmod +x start.sh

# Запуск
CMD ["./start.sh"]
