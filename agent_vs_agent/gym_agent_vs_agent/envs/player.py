import json
from gym_agent_vs_agent.envs.species import Species
from gym_agent_vs_agent.envs.moves import Moves
from gym_agent_vs_agent.envs.abilities import Abilities
from gym_agent_vs_agent.envs.items import Items
from gym_agent_vs_agent.envs.pokemon import Pokemon
import numpy as np
class Player():
    def __init__(self):
        self.forceSwitch = False

    def validMove(self, action):
        if action < 5 or self.trapped:
            if (action-1) in self.activeMoves:
                return action
            else:
                return (self.activeMoves[0]+1)
        else:
            if self.team[action-4].hp == 0:
                nextPokemon = self.nextActivePokemon()
                if nextPokemon == -1:
                    return (self.activeMoves[0]+1)
                else:
                    return (nextPokemon+3)
            else:
                return action

    def update(self, updateMessage):
        self.trapped = False
        updateDictionary = json.loads(updateMessage.split('|')[2])
        activeMoves = list()
        try:
            moves = updateDictionary['active'][0]['moves']
            for i in range(len(moves)):
                if moves[i]['pp'] > 0 and not moves[i]['disabled']:
                    activeMoves.append(i)
            self.activeMoves = activeMoves
            try:
                self.trapped = updateDictionary['active'][0]['maybeTrapped']
            except:
                try:
                    self.trapped = updateDictionary['active'][0]['trapped']
                except:
                    pass
        except KeyError:
            try:
                self.forceSwitch = updateDictionary['forceSwitch'][0]
            except KeyError:
                self.forceSwitch = False
                try:
                    self.trapped = updateDictionary['active'][0]['trapped']
                    self.activeMoves = [0]
                except KeyError:
                    self.activeMoves = [0]

        pokemonList = list()
        pokemonSummary = updateDictionary['side']['pokemon']
        for pokemon in pokemonSummary:
            species = Species[pokemon['details'][:pokemon['details'].find(',')].replace('-','_').replace(' ','_').replace("’",'').replace(":",'').replace('.','').replace('%','p')]
            if pokemon['condition'] == '0 fnt':
                hp = 0
            else:
                hp = int(pokemon['condition'][:pokemon['condition'].find('/')])
            moves = list()
            for move in pokemon['moves']:
                moves.append(Moves[move])
            if pokemon['item'] == '':
                item = -1
            else:
                item = Items[pokemon['item']]
            ability = Abilities[pokemon['ability']]
            pokemonList.append(Pokemon(species, hp, moves, item, ability))
        self.team = pokemonList

    def nextActivePokemon(self):
        for i in range(1, len(self.team)):
            if self.team[i].hp > 0:
                return (i+1)
        return -1

    def getTeam(self):
        return self.team

    def summarize(self):
        summaryVector = np.empty((1,1))
        for pokemon in self.team:
            pokeVec = pokemon.summarize()
            if not pokeVec.shape == (8,):
                print(pokeVec)
            summaryVector = np.concatenate([summaryVector, pokemon.summarize()], axis=None)
        return summaryVector

    def briefSummarize(self):
        summaryVector = np.empty((1,1))
        for pokemon in self.team:
            summaryVector = np.concatenate([summaryVector, pokemon.getHp()], axis=None)
        return summaryVector

