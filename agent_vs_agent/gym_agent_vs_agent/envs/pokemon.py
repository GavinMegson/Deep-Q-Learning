import numpy as np
class Pokemon():
    def __init__(self, species, hp, moves, item, ability):
        self.species = species
        self.hp = hp
        self.moves = moves
        self.item = item
        self.ability = ability

    def getHp(self):
        return self.hp

    def summarize(self):
        summaryVector = np.array([self.species.value, self.hp])
        for move in self.moves:
            summaryVector = np.concatenate([summaryVector, np.array([move.value])], axis=None)
        summaryVector = np.concatenate([summaryVector, np.array([self.item.value, self.ability.value])], axis=None)
        return summaryVector
