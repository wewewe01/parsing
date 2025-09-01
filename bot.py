import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8280789059:AAFokQ50dVGBTUOiY6DTY9zrRzbbvco7Iz4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://itv.uz/ru/anime")
    driver.implicitly_wait(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

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


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
