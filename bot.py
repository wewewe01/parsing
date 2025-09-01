import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = "8280789059:AAFokQ50dVGBTUOiY6DTY9zrRzbbvco7Iz4"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Используем requests вместо Selenium
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get("https://itv.uz/ru/anime", headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем карточки аниме
        cards = soup.select('.MuiGrid-item a')
        if not cards:
            await update.message.reply_text("Не удалось найти аниме.")
            return

        result = []
        for card in cards[:15]:  # первые 15 карточек
            try:
                title_elem = card.select_one('h2')
                title = title_elem.get_text(strip=True) if title_elem else "Нет названия"
                
                link = "https://itv.uz" + card.get('href', '')
                
                rating_elem = card.select_one('span.css-dibi8z')
                rating = rating_elem.get_text(strip=True) if rating_elem else "Нет рейтинга"
                
                result.append(f"<b>{title}</b>\nРейтинг: <i>{rating}</i>\n<a href='{link}'>Смотреть →</a>\n")
            except Exception as e:
                print(f"Ошибка обработки карточки: {e}")
                continue

        if result:
            text = "\n".join(result)
            await update.message.reply_text(text, parse_mode='HTML')
        else:
            await update.message.reply_text("Не удалось получить информацию об аниме.")
            
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
        print(f"Error: {e}")

# Добавляем обработчик
application.add_handler(CommandHandler("start", start_command))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        update = Update.de_json(data, application.bot)
        application.create_task(application.process_update(update))
        return 'OK'
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'Error', 500

@app.route('/')
def home():
    return 'Bot is running!'

@app.route('/set_webhook', methods=['GET'])
async def set_webhook_route():
    try:
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        result = await application.bot.set_webhook(webhook_url)
        return f'Webhook set to: {webhook_url} - {result}'
    except Exception as e:
        return f'Error setting webhook: {e}'

if __name__ == "__main__":
    # Устанавливаем webhook при запуске
    import asyncio
    
    async def setup():
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
        await application.bot.set_webhook(webhook_url)
        print(f"Webhook set to: {webhook_url}")
    
    asyncio.run(setup())
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
