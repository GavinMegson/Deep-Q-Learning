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
        summaryList = [self.species, self.health]
        for move in moves:
            summaryList += move.value
        summaryList += [item, ability]
        for stat in stats:
            summaryList += stat
        return np.array(summaryList)
