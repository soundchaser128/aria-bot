# pylint: disable=E1101

from typing import Callable, List, Optional, Tuple
from transitions import Machine
from enum import Enum
import random
from dataclasses import dataclass
from util import load_json

NAME_LISTS = load_json("data/name-parts.json")


def generate_slave_name(first_name: str, last_name: str) -> str:
    """
    Generates a name for the user.
    """
    first = random.choice(NAME_LISTS[first_name])
    last = random.choice(NAME_LISTS[last_name])
    return f"{first} {last}"


class State(Enum):
    Start = "start"
    AskingGender = "asking-gender"
    Greeting = "greeting"
    AssigningName = "assigning-name"
    AssigningNameConfimration = "assigining-name-confirmation"
    End = "end"


class Answer:
    message_key: str
    new_state: State
    action: Optional[Callable]

    def __init__(self, key: str, state: State, action: Optional[Callable]) -> None:
        self.message_key = key
        self.new_state = state
        self.action = action

    def __str__(self) -> str:
        return f"Answer(action={self.action}, message_key={self.message_key}, new_state={self.new_state})"

@dataclass
class AriaFsm:
    states = list(State)

    def __init__(self) -> None:
        self.machine = Machine(model=self, states=AriaFsm.states, initial=State.Start)
        self.machine.add_transition("ask_gender", State.Start, State.AskingGender)
        self.machine.add_transition(
            "assign_name", State.AskingGender, State.AssigningName
        )
        self.machine.add_transition(
            "assign_name_confirm", State.AssigningName, State.AssigningNameConfimration
        )
        self.machine.add_transition(
            "end", [State.AssigningNameConfimration, State.AssigningName], State.End
        )

    def step(self, user_input: List[str]) -> Answer:
        def set_gender(state):
            state.gender = "".join(user_input)

        def set_mood(state, mood: int, first: str, last: str):
            state.mood += mood
            state.slave_name = generate_slave_name(first, last)

        if self.state == State.Start:
            self.ask_gender()
            return Answer("gender_question", self.state, None)

        elif self.state == State.AskingGender:
            self.assign_name()
            return Answer("welcome.question", self.state, set_gender)

        elif self.state == State.AssigningName:
            if user_input == ["yes", "mistress"]:
                self.end()
                return Answer(
                    "welcome.answer_happy",
                    self.state,
                    lambda state: set_mood(state, 2, "first", "last"),
                )
            elif user_input == ["yes"]:
                self.assign_name_confirm()
                return Answer("welcome.answer_neutral", self.state, None)
            else:
                self.end()
                return Answer(
                    "welcome.answer_mad",
                    self.state,
                    lambda state: set_mood(state, -2, "bad", "bad"),
                )

        elif self.state == State.AssigningNameConfimration:
            if user_input == ["yes", "mistress"]:
                self.end()
                return Answer(
                    "welcome.answer_correct_answer",
                    self.state,
                    lambda state: set_mood(state, 1, "first", "last"),
                )
            else:
                self.end()
                return Answer(
                    "welcome.answer_incorrect_answer",
                    self.state,
                    lambda state: set_mood(state, -1, "bad", "last"),
                )

        else:
            return Answer("end_message", self.state, None)
