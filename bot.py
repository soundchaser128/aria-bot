import discord
import os
from discord.embeds import Embed
from dotenv import load_dotenv
import logging
from state import State, UserState
from typing import Dict
import asyncio

class AriaBot(discord.Client):
    user_states: Dict[int, UserState] = {}

    async def on_ready(self):
        logging.info("bot is ready!")
        pass

    def _filter_message(self, message: discord.Message) -> bool:
        return type(message.channel) is discord.DMChannel and not message.author.bot

    def _create_embed(self, msg: str, state: State) -> Embed:
        embed = Embed(
            title="ARIA",
            description=msg,
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_image(url="https://media.discordapp.net/attachments/643335030617407488/733402800360521788/Domme_Cara.jpg?width=652&height=864")
        return embed

    async def on_message(self, message: discord.Message):
        if self._filter_message(message):
            logging.info("received message %s", message.content)
            user_id = message.author.id
            state = None
            try:
                state = self.user_states[user_id]
            except KeyError:
                state = UserState(user_id, message.author.name)
                self.user_states[user_id] = state
            messages = state.next(message.content)
            channel = message.channel
            for msg in messages:
                await channel.send(embed=self._create_embed(msg, state.current))
                await asyncio.sleep(2)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    load_dotenv()
    token = os.environ["ARIA_BOT_TOKEN"]

    bot = AriaBot()
    bot.run(token)
