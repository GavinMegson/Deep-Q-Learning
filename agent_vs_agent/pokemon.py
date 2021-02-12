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
        summary_list = [self.species, self.health]
        for move in moves:
            summary_list += move.value
        summary_list += [item, ability]
        for stat in stats:
            summary_list += stat
