from enum import Enum, auto
import logging
from typing import List, Optional
import re
import json
import random


def load_names():
    with open("name-parts.json") as fp:
        return json.load(fp)


WORD_REGEX = re.compile("([^a-z]+)", re.UNICODE)
SPACE_REGEX = re.compile(r"\s+")
NAME_LISTS = load_names()


def generate_slave_name(first_name: str, last_name: str) -> str:
    """
    Generates a name for the user.
    """
    first = random.choice(NAME_LISTS[first_name])
    last = random.choice(NAME_LISTS[last_name])
    return f"{first} {last}"

def clean_input(input: str) -> List[str]:
    """
    Converts the input into a list of lower-case tokens with all non-alphabetic characters removed.
    """
    tokens = SPACE_REGEX.split(input.strip().lower())
    return [WORD_REGEX.sub("", s) for s in tokens]


# TODO this approach probably won't scale well
class State(Enum):
    AskGender = 0
    GreetingUser = 1
    FirstQuestion = 2
    FirstQuestionConfirmation = 3
    End = auto


class UserState:
    """
    Encapsulates the entire game state for a single user. State machine-ish.
    """
    user_id: int
    user_name: str
    current: State
    mood: int

    slave_name: Optional[str]
    gender: Optional[str]

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.current = State.AskGender
        self.mood = 0
        self.slave_name = None
        self.gender = None

    def next(self, user_input: str) -> str:
        """
        Takes the user's input and advances the state based on it. Returns
        the text the bot should answer in response.
        """
        logging.info("received input %s for user %s", user_input, self.user_name)

        if self.current == State.AskGender:
            self.current = State.GreetingUser
            return "Before we get started, would you rather I call you a **boy** or a **girl**?"

        elif self.current == State.GreetingUser:
            self.current = State.FirstQuestion
            self.gender = clean_input(user_input)[0]
            return f"""
                Hello {self.user_name}, I am ARIA and I'm your new Mistress.
                For this session, don't you think we should call you something more appropriate?
            """

        elif self.current == State.FirstQuestion:
            tokens = clean_input(user_input)
            logging.info("parsed input into %s", tokens)

            if tokens == ["yes", "mistress"]:
                self.mood += 2
                self.slave_name = generate_slave_name("first", "last")
                self.current = State.End
                return f"""
                    Good {self.gender}! That's the correct answer.
                    I've decided to name you **{self.slave_name}** because you're a good little {self.gender} who's eager to please.
                """
            elif tokens == ["yes"]:
                # TODO
                self.current = State.FirstQuestionConfirmation
                return "Close. Yes *what?*"
            else:
                self.mood -= 2
                self.slave_name = generate_slave_name("bad", "bad")
                self.current = State.End
                return f"""
                    Hmmm. That's a shame. You're off to a bad start, but I'll train you up.
                    A "yes" or "yes mistress" should have been easy, but you had to get mouthy.
                    So your new name is **{self.slave_name}** and you'll see what that means if you don't improve your attitude.
                """
        elif self.current == State.FirstQuestionConfirmation:
            tokens = clean_input(user_input)

            if tokens == ["yes", "mistress"]:
                self.mood += 1
                self.slave_name = generate_slave_name("first", "last")
                self.current = State.End
                return f"""
                    Good {self.gender}! You got there. That's the correct answer.
                    I've decided to name you **{self.slave_name}** because you're a good little {self.gender} who's eager to please.
                """
            else:
                self.mood -= 1
                self.slave_name = generate_slave_name("bad", "last")
                self.current = State.End
                return f"""
                    Hmmm. That's a shame you didn't pick up on my hint. You're off to a bad start, but I'll train you up.
                    I've decided to name you **{self.slave_name}** because you're almost getting the idea but seem a little slow.
                """
                
        else:
            return "That's it for now!"
