FROM python:3.10-slim

# Установка системных зависимостей и Chrome
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip ca-certificates \
    fonts-liberation libnss3 libxss1 libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 xvfb \
    && rm -rf /var/lib/apt/lists/*

# Добавление репозитория Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

# Установка Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Установка ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver.zip

# Установка зависимостей Python
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Разрешаем запуск start.sh
RUN chmod +x start.sh

# Запуск
CMD ["./start.sh"]
