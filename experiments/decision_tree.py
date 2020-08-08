from typing import Callable, List, Optional


class State:
    mood: int
    user_name: str
    user_id: int

    gender: Optional[str]
    slave_name: Optional[str]

    def __init__(self, user_id: int, user_name: str) -> None:
        self.mood = 0
        self.user_id = user_id
        self.user_name = user_name

        self.gender = None
        self.slave_name = None


class Node:
    name: str
    children: List["Node"]
    condition: Callable[[State, str], bool]
    action: Optional[Callable[[State, str], None]]
    message: str

    def __init__(
        self,
        name: str,
        condition: Optional[Callable[[State, str], bool]],
        action: Callable,
        message: str,
        children: List["Node"],
    ) -> None:
        self.name = name
        self.children = children
        self.condition = condition
        self.action = action
        self.message = message

    def execute(self, state: State, answer: str) -> Optional[str]:
        if self.condition(state, answer):
            if self.action:
                self.action(state, answer)
            return self.message
        else:
            return None


class Executor:
    state: State
    current_node: Node
    iteration: int

    def __init__(self, user_id: int, user_name: str, tree: Node) -> None:
        self.state = State(user_id, user_name)
        self.current_node = tree
        self.iteration = 0

    def execute(self, answer: str) -> Optional[str]:
        response = self.current_node.execute(self.state, answer)
        if response:
            return response
        else:
            return None

    def next(self, answer: str) -> Optional[None]:
        child = None
        for node in self.current_node.children:
            if node.condition(self.state, answer):
                child = node
                break

        if child is not None:
            self.current_node = child
            self.iteration += 1
            return child
        else:
            return None
