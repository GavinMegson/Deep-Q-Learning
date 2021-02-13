import numpy as np
class Pokemon:
    def __init__(self, species, moves, item, ability, stats):
        self.species = species
        self.hp = 100
        self.moves = moves
        self.moveStatus = len(moves)*[True]
        self.item = item
        self.ability = ability
        self.stats = stats

    def getHp(self):
        return self.hp

    def setHp(self, hp):
        self.hp = hp

    def setMoveStatus(self, index, status):
        self.moveStatus[index] = status

    def validMove(self, index):
        return self.moveStatus[index]

    def summarize(self):
        summaryList = [self.species, self.hp]
        for move in self.moves:
            summaryList.append(move.value)
        summaryList += [self.item, self.ability]
        for stat in self.stats:
            summaryList.append(stat)
        return np.array(summaryList)
