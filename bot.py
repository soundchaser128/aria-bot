import discord
import os
from dotenv import load_dotenv
import logging
from state import UserState
from typing import Dict

class AriaBot(discord.Client):
    user_states: Dict[int, UserState]  = {}

    async def on_ready(self):
        logging.info("bot is ready!")
        pass

    def _filter_message(self, message: discord.Message) -> bool:
        return type(message.channel) is discord.DMChannel and not message.author.bot

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
            state.next(message.content)
                


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    load_dotenv()
    token = os.environ["ARIA_BOT_TOKEN"]

    bot = AriaBot()
    bot.run(token)
