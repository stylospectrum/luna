import aiohttp
import discord

from config.settings import settings

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = discord.Client(intents=intents)
url = f'http://localhost:{settings.PORT}/predict'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    message = await message.channel.fetch_message(message.id)
    data = {
        'user_id': message.author.name,
        'content': message.content
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_content = await response.json()

    await message.reply(json_content['content'])

bot.run(settings.DISCORD_BOT_TOKEN)
