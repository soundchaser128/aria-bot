from decision_tree import Executor, Node, State


def set_gender(state: State, answer: str):
    state.gender = answer.strip()

tree = Node(
    'ask-gender',
    lambda state, answer: True,
    set_gender,
    "gender_question",
    [
        Node(
            'welcome',
            lambda state, answer: True,
            None,
            'welcome_question',
            []
        ),
    ]
)
class FakeClient:
    game_states = {}

    def get_state(self, user_id, user_name): 
        try:
            return self.game_states[user_id]
        except KeyError:
            state = Executor(user_id, user_name, tree)
            self.game_states[user_id] = state
            return state

    def on_message(self, user_id, user_name, message_content):
        state = self.get_state(user_id, user_name)
        prompt = state.execute(message_content)
        if state.iteration > 0:
            state.next(message_content)
        return prompt


def test_execute():
    executor = Executor(1, 'name', tree)

    answer = executor.execute('boy')
    assert answer == 'gender_question'
    assert executor.state.gender == 'boy'
    
def test_fake_client():
    client = FakeClient()

    answer1 = client.on_message(1, 'name', 'boy')
    assert answer1 == 'gender_question'