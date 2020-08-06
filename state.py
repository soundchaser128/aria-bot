from enum import Enum
import logging
from typing import List, Optional
import re
import json
import random


def load_names():
    with open("name-parts.json") as fp:
        return json.load(fp)


WORD_REGEX = re.compile("([^a-z]+)", re.UNICODE)
SPACE_REGEX = re.compile("\s+")
NAME_LISTS = load_names()


def generate_slave_name(first_name: str, last_name: str) -> str:
    first = random.choice(NAME_LISTS[first_name])
    last = random.choice(NAME_LISTS[last_name])
    return f"{first} {last}"


# FIXME
def clean_input(input: str) -> List[str]:
    tokens = SPACE_REGEX.split(input.strip().lower())
    return [WORD_REGEX.sub("", s) for s in tokens]


class State(Enum):
    Start = 0
    GreetingUser = 1
    FirstQuestion = 2


class UserState:
    user_id: int
    user_name: str
    current: State
    mood: int

    slave_name: Optional[str]

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.current = State.Start
        self.mood = 0
        self.slave_name = None

    def next(self, user_input: str) -> str:
        logging.info("received input %s for user %s", user_input, self.user_name)

        if self.current == State.Start:
            self.current = State.GreetingUser
            return f"""
                Hello {self.user_name}, I am ARIA and I'm your new Mistress.
                For this session, don't you think we should call you something more appropriate?
            """

        elif self.current == State.GreetingUser:
            tokens = clean_input(user_input)
            logging.info("parsed input into %s", tokens)

            if tokens == ["yes", "mistress"]:
                self.mood += 2
                self.slave_name = generate_slave_name("first", "last")
                return f"""
                    Good boy! That's the correct answer.
                    I've decided to name you **{self.slave_name}** because you're a good little boy who's eager to please.
                """
            elif tokens == ["yes"]:
                # TODO
                self.current = State.FirstQuestion
                return "Close. Yes *what?*"
            else:
                self.mood -= 2
                self.slave_name = generate_slave_name("bad", "bad")
                return f"""
                    A "yes" or "yes mistress" should have been easy, but you had to get mouthy.
                    So your new name is **{self.slave_name}** and you'll see what that means if you don't improve your attitude.
                """
        elif self.current == State.FirstQuestion:
            # TODO
            return "TODO"
        else:
            return "That's it for now!"
