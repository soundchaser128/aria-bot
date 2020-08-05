import discord
import os
from discord.embeds import Embed
from dotenv import load_dotenv
import logging
from state import UserState
from typing import Dict


class AriaBot(discord.Client):
    user_states: Dict[int, UserState] = {}

    async def on_ready(self):
        logging.info("bot is ready!")
        pass

    def _filter_message(self, message: discord.Message) -> bool:
        return type(message.channel) is discord.DMChannel and not message.author.bot

    def _create_embed(self, msg: str, state: UserState) -> Embed:
        embed = Embed(
            title="ARIA", description=msg, color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.add_field(name="Mistress Mood", value=str(state.mood))
        embed.set_image(
            url="https://media.discordapp.net/attachments/643335030617407488/733402800360521788/Domme_Cara.jpg?width=652&height=864"
        )
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
            text = state.next(message.content)
            await message.channel.send(embed=self._create_embed(text, state))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    load_dotenv()
    token = os.environ["ARIA_BOT_TOKEN"]

    bot = AriaBot()
    bot.run(token)
