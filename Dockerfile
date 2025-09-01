FROM python:3.10-slim

RUN pip install webdriver-manager==3.8.5
RUN python - << 'EOF'
from webdriver_manager.chrome import ChromeDriverManager
from os import environ
print(ChromeDriverManager().install())
EOF


# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 lsb-release fonts-liberation \
    libnss3 libxss1 libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 xvfb \
    ca-certificates

# 2. Добавляем репозиторий Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

# 3. Устанавливаем Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# 4. Установка ChromeDriver (автоматически под совместимую версию)
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver.zip

# 5. Копируем проект и устанавливаем Python-зависимости
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Разрешаем выполнение start.sh
RUN chmod +x start.sh

# 7. Команда запуска
CMD ["./start.sh"]

