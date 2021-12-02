from random import randint, uniform


class RandomAgent():
    def predict(self, obs):
        if uniform(0, 1) < 0.9:
            return (randint(1, 4), 0)
        return (randint(5, 9), 0)
