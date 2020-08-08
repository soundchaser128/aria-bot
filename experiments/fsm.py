from typing import Optional
from transitions import Machine
from enum import Enum


class State(Enum):
    Start = "start"
    AskingGender = "asking-gender"
    Greeting = "greeting"
    AssigningName = "assigning-name"
    AssigningNameConfimration = "assigining-name-confirmation"


class Aria:
    states = list(State)
    mood: int

    gender: Optional[str]

    def __init__(self, user_id: int, user_name: str) -> None:
        self.mood = 0
        self.user_id = user_id
        self.user_name = user_name
        self.gender = None

        self.machine = Machine(model=self, states=Aria.states, initial=State.Start)
        self.machine.add_transition("ask_gender", State.Start, State.AskingGender)
        # TODO?
