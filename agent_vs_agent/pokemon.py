import numpy as np
class Pokemon:
    def __init__(self, species, moves, item, ability, stats):
        self.species = species
        self.hp = 100
        self.moves = moves
        self.item = item
        self.ability = ability
        self.stats = stats

    def summarize(self):
        summaryList = [self.species, self.hp]
        for move in self.moves:
            summaryList.append(move.value)
        summaryList += [self.item, self.ability]
        for stat in self.stats:
            summaryList.append(stat)
        print(np.array(summaryList))
        return np.array(summaryList)
