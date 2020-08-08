# pylint: disable=E1101

from state import clean_input, Aria, message
from fsm import State
import re
import pickle


def test_clean_input():
    expected = ["yes", "mistress"]
    assert clean_input(" yes, mistress! ") == expected
    assert clean_input("yes mistress") == expected
    assert clean_input("yes,mistress") == expected


def test_state_transitions():
    aria = Aria(1, "test")
    assert aria.fsm.state == State.Start
    assert aria.mood == 0
    assert aria.user_id == 1
    assert aria.user_name == "test"

    question = aria.next(None)
    assert question == message("gender_question")
    assert aria.fsm.state == State.AskingGender
    
    question = aria.next("boy")
    assert question == message("welcome.question", user_name="test")
    assert aria.fsm.state == State.AssigningName

    question = aria.next("yes")
    assert question == message("welcome.answer_neutral")
    assert aria.fsm.state == State.AssigningNameConfimration

    question = aria.next("yes mistress")
    assert re.match(r"[a-z]+\s[a-z]+", aria.slave_name)
    
    question = question.replace(aria.slave_name, "fake name")
    assert question == message("welcome.answer_correct_answer", gender="boy", slave_name="fake name")
    assert aria.mood == 1


def test_serialization():
    aria = Aria(1, "test")
    ser = pickle.dumps(aria)
    assert ser is not None

    result = pickle.loads(ser)
    assert aria == result
