from enum import Enum
import logging

class State(Enum):
    Start = 0
    ChooseName = 1


class UserState:
    user_id: int
    user_name: str
    current: State

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.current = State.Start

    def next(self, input: str):
        logging.info('received input %s for user %s', input, self.user_name)