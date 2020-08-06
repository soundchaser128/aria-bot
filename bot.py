import os
import logging
from typing import Dict
import discord
from discord.activity import Game
from dotenv import load_dotenv
from discord.embeds import Embed
from state import UserState

PREFIX = "!"
IMAGES = {
    "neutral": "https://media.discordapp.net/attachments/643335030617407488/733402800360521788/Domme_Cara.jpg?width=652&height=864",
    "strict": "https://media.discordapp.net/attachments/643335030617407488/733782996011712512/ARIA_Strict.jpg?width=641&height=849"
}
HELP_MESSAGE = """
**ARIA**
Virtual mistress. You must be 18 or older to continue.

Enter any text to start a game or to answer the bot's questions.

Commands:
* `!reset`: Reset your game to the beginning.
* `!cleanup`: Remove all the bot's messages.
* `!help`: To view this help message.
"""

class AriaBot(discord.Client):
    # TODO load from/save to database eventually (for persistence across restarts)
    user_states: Dict[int, UserState] = {}

    async def on_ready(self):
        await self.change_presence(status= Game(name="DM me to get started!"))
        logging.info("bot is ready!")

    def create_embed(self, msg: str, state: UserState) -> Embed:
        image = "neutral"
        if state.mood < 0:
            image = "strict"
        embed = Embed(
            title="ARIA", description=msg, color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.add_field(name="Mistress Mood", value=str(state.mood))
        embed.set_image(
            url=IMAGES[image]
        )
        return embed

    async def do_cleanup(self, message: discord.Message, user_id: int):
        logging.info("cleaning up bot messages for user %s", user_id)
        async for message in message.channel.history(limit=200):
            if message.author.id == self.user.id:
                logging.info("deleting message %s", message.id)
                await message.delete()

    async def on_message(self, message: discord.Message):
        should_process = isinstance(message.channel, discord.DMChannel) and not message.author.bot
        
        if should_process:
            content: str = message.content
            user_id = message.author.id
            user_name = message.author.name
            logging.info("received message '%s' from user '%s'", content, user_name)

            if content.startswith(PREFIX):
                if content == "!cleanup":
                    await self.do_cleanup(message, user_id)
                elif content == "!reset":
                    self.user_states[user_id] = UserState(user_id, user_name)                    
                elif content == "!help":
                    await message.channel.send(HELP_MESSAGE)
            else:
                state = None
                try:
                    state = self.user_states[user_id]
                except KeyError:
                    state = UserState(user_id, user_name)
                    self.user_states[user_id] = state
                text = state.next(message.content)
                await message.channel.send(embed=self.create_embed(text, state))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    load_dotenv()
    token = os.environ["ARIA_BOT_TOKEN"]

    bot = AriaBot()
    bot.run(token)
