from species import Species
from moves import Moves
from items import Items
from ability_lookup import AbilityLookup
from abilities import Abilities
from actions import Actions
from pokemon import Pokemon
from random import choice

class Player():
    def __init__(self, name, team, order="12345"):
        self.name = name
        self.packedTeam = team
        self.processTeam(team)
        self.order = order
        self.setActivePokemon(int(order[0]))

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team

    def getPackedTeam(self):
        return self.packedTeam

    def getOrder(self):
        return self.order

    def getMove(self, match):
        potentialActions = list()
        for action in Actions:
            if (action > Actions.Switch6 and self.validMove(action-Actions.Switch6-1)) or (action < Actions.Move1 and self.getPokemonHp(action.value) != 0):
                potentialActions.append(action)
        return choice(potentialActions)

    def setMoveStatus(self, action, status):
        self.team[0].setMoveStatus(action, status)

    def validMove(self, action):
        return self.team[0].validMove(action)

    def forceSwitch(self, match):
        potentialActions = list()
        for action in Actions:
            if action < Actions.Move1 and self.getPokemonHp(action.value) != 0:
                potentialActions.append(action)
        return choice(potentialActions)


    def setActivePokemon(self, index):
        temp = self.team[0]
        self.team[0] = self.team[index-1]
        self.team[index-1] = temp

    def getPokemonHp(self, index):
        return self.team[index-1].getHp()

    def updatePokemonHealth(self, hp):
        self.team[0].setHp(hp)

    def processTeam(self, team):
        self.team = list()
        team = team.split(']')
        for pokemonInfo in team:
            pokemonInfo = pokemonInfo.split('|')
            species = Species[pokemonInfo[0]]
            moveList = list()
            for move in pokemonInfo[4].split(','):
                moveList.append(Moves[move])
            item = Items[pokemonInfo[2]]
            abilityArray = AbilityLookup[species.name].value['abilities']
            try:
                if pokemonInfo[3] == "":
                    abilityIndex = 0
                else:
                    abilityIndex = int(pokemonInfo[3])
            except:
                abilityIndex = pokemonInfo[3]
            ability = abilityArray[abilityIndex].replace(" ", "").lower()
            ability = Abilities[ability]
            statList = list()
            for stat in pokemonInfo[6].split(','):
                if stat == '':
                    stat = 0
                statList.append(int(stat))
            self.team.append(Pokemon(species.value, moveList, item.value, ability.value, statList))



team = "Lumineon||focussash|1|defog,scald,icebeam,uturn||85,85,85,85,85,85||||83|]Glaceon||lifeorb||toxic,hiddenpowerground,shadowball,icebeam||81,,85,85,85,85||,0,,,,||83|]Crabominable||choiceband|1|closecombat,earthquake,stoneedge,icehammer||85,85,85,85,85,85||||83|]Toxicroak||lifeorb|1|drainpunch,suckerpunch,gunkshot,substitute||85,85,85,85,85,85||||79|]Bouffalant||choiceband||earthquake,megahorn,headcharge,superpower||85,85,85,85,85,85||||83|]Qwilfish||blacksludge|H|thunderwave,destinybond,liquidation,painsplit||85,85,85,85,85,85||||83|"

p = Player("alice", team)

