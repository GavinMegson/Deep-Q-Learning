import json
from species import Species
from moves import Moves
from abilities import Abilities
from items import Items
from pokemon import Pokemon
import numpy as np
class Player():
    def update(self, updateMessage):
        updateDictionary = json.loads(updateMessage.split('|')[2])
        activeMoves = list()
        moves = updateDictionary['active'][0]['moves']
        for i in range(len(moves)):
            if moves[i]['pp'] > 0 and not moves[i]['disabled']:
                activeMoves.append(i)
        self.activeMoves = activeMoves

        pokemonList = list()
        pokemonSummary = updateDictionary['side']['pokemon']
        for pokemon in pokemonSummary:
            species = Species[pokemon['details'][:pokemon['details'].find(',')].replace('-','_').replace(' ','_').replace("`",'').replace('.','').replace('%','p')]
            if pokemon['condition'] == '0 fnt':
                hp = 0
            else:
                hp = pokemon['condition'][:pokemon['condition'].find('/')]
            moves = list()
            for move in pokemon['moves']:
                moves.append(Moves[move])
            item = Items[pokemon['item']]
            ability = Abilities[pokemon['ability']]
            pokemonList.append(Pokemon(species, hp, moves, item, ability))
        self.team = pokemonList

    def getTeam(self):
        return self.team

    def summarize(self):
        summaryVector = np.empty((1,1))
        for pokemon in self.team:
            summaryVector = np.concatenate([summaryVector, pokemon.summarize()], axis=None)
        return summaryVector

    def briefSummarize(self):
        summaryVector = np.empty((1,1))
        for pokemon in self.team:
            summaryVector = np.concatenate([summaryVector, pokemon.getHp()], axis=None)
        return summaryVector

