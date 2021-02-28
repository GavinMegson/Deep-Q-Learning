import numpy as np
class Pokemon():
    def __init__(self, species, hp, moves, item, ability):
        self.species = species
        self.hp = hp
        self.moves = moves
        while not len(self.moves) == 4:
            self.moves.append(-1)
        self.item = item
        self.ability = ability

    def getHp(self):
        return self.hp

    def summarize(self):
        summaryVector = np.array([self.species.value, self.hp])
        for move in self.moves:
            if move == -1:
                moveValue = -1
            else:
                moveValue = move.value
            summaryVector = np.concatenate([summaryVector, np.array([moveValue])], axis=None)
        if self.item == -1:
            itemValue = -1
        else:
            itemValue = self.item.value
        summaryVector = np.concatenate([summaryVector, np.array([itemValue, self.ability.value])], axis=None)
        return summaryVector
