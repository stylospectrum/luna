import logging
import aiohttp

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

from config.settings import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

url = f'http://localhost:{settings.PORT}/predict'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    data = {
        'user_id': str(update.effective_chat.id),
        'content': update.message.text.replace("/luna", "").strip()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_content = await response.json()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=json_content['content'], )


if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('luna', reply)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), reply)
    application.add_handler(echo_handler)

    application.run_polling()
