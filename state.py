import json
import logging
from typing import List, Optional
import re
from dataclasses import dataclass
from util import load_json
from fsm import AriaFsm


WORD_REGEX = re.compile("([^a-z]+)", re.UNICODE)
SPACE_REGEX = re.compile(r"[\s|,.!|]+")
MESSAGES = load_json("data/messages.json5")


def clean_input(input: Optional[str]) -> List[str]:
    """
    Converts the input into a list of lower-case tokens with all non-alphabetic characters removed.
    """
    if input is None:
        return []
    tokens = SPACE_REGEX.split(input.strip().lower())
    return [WORD_REGEX.sub("", s) for s in tokens if len(s) > 0]


def message(key: str, **args) -> str:
    """
    Takes a path like `welcome.question` and does a lookup in the message.json5 file. Also 
    replaces placeholders like {user_name} with the values passed in via keyword arguments.
    """
    path = key.split(".")
    path.reverse()
    ptr = MESSAGES
    while len(path) > 0:
        k = path.pop()
        ptr = ptr[k]
    assert isinstance(ptr, str)
    return ptr.format(**args)

@dataclass
class Aria:
    """
    Encapsulates the entire game state for a single user.
    """

    user_id: int
    user_name: str
    mood: int
    fsm: AriaFsm

    slave_name: Optional[str]
    gender: Optional[str]

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.mood = 0
        self.slave_name = None
        self.gender = None
        self.fsm = AriaFsm()

    def _message_args(self):
        return {
            "gender": self.gender,
            "slave_name": self.slave_name,
            "user_name": self.user_name,
        }

    def next(self, user_input: str) -> str:
        tokens = clean_input(user_input)
        answer = self.fsm.step(tokens)
        logging.info("fsm produced output %s", answer)

        if answer.action:
            answer.action(self)

        return message(answer.message_key, **self._message_args())
