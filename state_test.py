from state import clean_input, Aria, State, message


def test_clean_input():
    expected = ["yes", "mistress"]
    assert clean_input(" yes, mistress! ") == expected
    assert clean_input("yes mistress") == expected
    assert clean_input("yes,mistress") == expected


def test_state_transitions():
    aria = Aria(1, "test")
    assert aria.current == State.AskGender
    assert aria.mood == 0

    first_question = aria.next(None)
    assert first_question == message("gender_question")
    