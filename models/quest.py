class Quest:
    def __init__(self, id, description, reward, required_level):
        self.id = id
        self.description = description
        self.reward = reward
        self.required_level = required_level