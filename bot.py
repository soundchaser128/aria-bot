import discord
import os
from dotenv import load_dotenv

class AriaBot(discord.Client):
    async def on_ready(self):
        pass

if __name__ == '__main__':
    load_dotenv()
    token = os.environ['ARIA_BOT_TOKEN']

    bot = AriaBot()
    bot.run(token)
