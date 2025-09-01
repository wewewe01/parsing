import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = "8280789059:AAFokQ50dVGBTUOiY6DTY9zrRzbbvco7Iz4"

# Создаем Flask приложение
app = Flask(__name__)

# Инициализируем Telegram Application
application = Application.builder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://itv.uz/ru/anime")
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        cards = soup.select(".MuiGrid-root.MuiGrid-item a")
        if not cards:
            await update.message.reply_text("Не удалось получить список аниме.")
            return

        result = []
        for card in cards:
            title_teg = card.select_one("h2")
            if not title_teg:
                continue

            title = title_teg.get_text(strip=True) if title_teg else "—"
            if not title:
                continue

            link = "https://itv.uz" + card["href"]
            rating = card.select_one("span.css-dibi8z")
            rating = rating.get_text(strip=True) if rating else ""

            result.append(f"<b>{title}</b>\nРейтинг: <i>{rating}</i>\n<a href='{link}'>Смотреть →</a>\n")

        text = "\n".join(result[:15])  # ограничим первыми 15
        await update.message.reply_text(text, parse_mode="HTML")
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
        
    finally:
        driver.quit()

# Добавляем обработчик
application.add_handler(CommandHandler("start", start_command))

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        data = await request.get_json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return 'OK'
    except Exception as e:
        print(f"Error processing update: {e}")
        return 'Error', 500

# Health check endpoint
@app.route('/')
def index():
    return 'Bot is running!'

async def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await application.bot.set_webhook(webhook_url)

if __name__ == "__main__":
    # Устанавливаем webhook при запуске
    import asyncio
    asyncio.run(set_webhook())
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
