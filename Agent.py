from Serializer import vec_state, devec_action

class Agent:
    def __init__(self, currentModel) -> None:
        self.model = currentModel

    def takeBestAction(self, state) -> None:
        state.play(devec_action(self.model(vec_state(state))))

