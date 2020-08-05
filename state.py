from enum import Enum
import logging
from typing import List


class State(Enum):
    Start = 0
    GreetingUser = 1


class UserState:
    user_id: int
    user_name: str
    current: State

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.current = State.Start

    def next(self, input: str) -> List[str]:
        logging.info("received input %s for user %s", input, self.user_name)

        if self.current == State.Start:
            self.current = State.GreetingUser
            return [
                f"Hello {self.user_name}, I am ARIA and I'm your new Mistress\nFor this session, don't you think we should call you something more appropriate?",
            ]

        else:
            return ["That's it for now"]
