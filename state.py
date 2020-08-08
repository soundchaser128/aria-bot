from enum import Enum, auto
import logging
from typing import List, Optional
import re
import random
from util import load_json


WORD_REGEX = re.compile("([^a-z]+)", re.UNICODE)
SPACE_REGEX = re.compile(r"[\s|,.!|]+")
NAME_LISTS = load_json("data/name-parts.json")
MESSAGES = load_json("data/messages.json5")


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
    return [WORD_REGEX.sub("", s) for s in tokens if len(s) > 0]


def message(key: str, **args) -> str:
    path = key.split(".")
    path.reverse()
    ptr = MESSAGES
    while len(path) > 0:
        k = path.pop()
        ptr = ptr[k]
    assert isinstance(ptr, str)
    return ptr.format(**args)


# TODO this approach probably won't scale well
class State(Enum):
    AskGender = 0
    GreetingUser = 1
    FirstQuestion = 2
    FirstQuestionConfirmation = 3
    End = auto


class Aria:
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

    def next(self, user_input: Optional[str]) -> str:
        """
        Takes the user's input and advances the state based on it. Returns
        the text the bot should answer in response.
        """
        logging.info("received input %s for user %s", user_input, self.user_name)

        if self.current == State.AskGender:
            self.current = State.GreetingUser
            return message("gender_question")

        elif self.current == State.GreetingUser:
            self.current = State.FirstQuestion
            self.gender = clean_input(user_input)[0]
            return message("welcome.question", user_name=self.user_name)

        elif self.current == State.FirstQuestion:
            tokens = clean_input(user_input)
            logging.info("parsed input into %s", tokens)

            if tokens == ["yes", "mistress"]:
                self.mood += 2
                self.slave_name = generate_slave_name("first", "last")
                self.current = State.End
                return message(
                    "welcome.answer_happy",
                    gender=self.gender,
                    slave_name=self.slave_name,
                )
            elif tokens == ["yes"]:
                self.current = State.FirstQuestionConfirmation
                return message("welcome.answer_neutral")
            else:
                self.mood -= 2
                self.slave_name = generate_slave_name("bad", "bad")
                self.current = State.End
                return message("welcome.answer_mad", slave_name=self.slave_name)
        elif self.current == State.FirstQuestionConfirmation:
            tokens = clean_input(user_input)

            if tokens == ["yes", "mistress"]:
                self.mood += 1
                self.slave_name = generate_slave_name("first", "last")
                self.current = State.End
                return message(
                    "welcome.answer_correct_answer",
                    gender=self.gender,
                    slave_name=self.slave_name,
                )
            else:
                self.mood -= 1
                self.slave_name = generate_slave_name("bad", "last")
                self.current = State.End
                return message(
                    "welcome.answer_incorrect_answer", slave_name=self.slave_name
                )

        else:
            return "That's it for now!"
