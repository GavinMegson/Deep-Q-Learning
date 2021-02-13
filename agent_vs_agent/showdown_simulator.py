import subprocess
from random import randint
import pexpect
from player import Player
from time import sleep
from species import Species
from match import Match
from actions import Actions
from json import loads
import sys

class ShowdownSimulator():
    def __init__(self):
        self.process = pexpect.spawn('/home/wlayton/pokemon-showdown/pokemon-showdown simulate-battle',encoding='utf-8')
        self.process.logfile_read = sys.stdout
        #self.process.logfile = None

    def summary(self, player):
        return self.match.summarize(player)
        
    def setup(self, p1, p2):
        self.match = Match(p1, p2)
        self.process.send('>start {"formatid":"gen8ou"}\n')
        self.process.expect('update')

        self.process.send('>player p1 {"name":"%s", "team":"%s"}\n' % (p1.getName(), p1.getPackedTeam()))
        self.process.expect('update')

        self.process.sendline('>player p2 {"name":"%s", "team":"%s"}' % (p2.getName(), p2.getPackedTeam()))
        self.process.expect('update')

        self.process.sendline('>p1 team {0}'.format(p1.getOrder()))
        p1.setActivePokemon(int(p1.getOrder()[0]))
        self.process.expect('update')

        self.process.sendline('>p2 team {0}'.format(p2.getOrder()))
        p2.setActivePokemon(int(p2.getOrder()[0]))
        self.process.expect('update')
        
    def update(self, p1, p2):
        p1Action = p1.getMove(self.summary(p1))
        p2Action = p2.getMove(self.summary(p2))
        if p1Action < Actions.Move1:
            self.process.sendline(f">p1 switch {p1Action.value}")
            p1.setActivePokemon(p1Action.value)
        else:
            self.process.sendline(f">p1 move {p1Action.value-Actions.Switch6.value}")

        if p2Action < Actions.Move1:
            self.process.sendline(f">p2 switch {p2Action.value}")
            p2.setActivePokemon(p2Action.value)
        else:
            self.process.sendline(f">p2 move {p2Action.value-Actions.Switch6.value}")
        self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")
        p1Update = self.process.match.group(1)
        p1Update = p1Update.split('|')
        #print(p1Update[2])
        p1Update = loads(p1Update[2])
        try:
            forceSwitch = p1Update['forceSwitch'][0]
        except KeyError:
            forceSwitch = False
            for (move, index) in zip(p1Update['active'][0]['moves'], range(1,5)):
                p1.setMoveStatus(index-1,not(move['disabled']) and move['pp'] != 0)
        for pokemon in p1Update['side']['pokemon']:
            if pokemon['active']:
                hp = pokemon['condition']
                if hp == "0 fnt":
                    newHp = 0
                else:
                    newHp = int(pokemon['condition'][:pokemon['condition'].find('/')])
                p1.updatePokemonHealth(newHp)
        if forceSwitch:
            p1Switch = p1.forceSwitch(self.summary(p1))
            self.process.sendline(f">p1 switch {p1Switch.value}")
            self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")


        p2Update = self.process.match.group(2)
        p2Update = p2Update.split('|')
        p2Update = loads(p2Update[2])
        try:
            forceSwitch = p2Update['forceSwitch'][0]
        except KeyError:
            forceSwitch = False
            for (move, index) in zip(p2Update['active'][0]['moves'], range(1,5)):
                p2.setMoveStatus(index-1, not(move['disabled']) and move['pp'] != 0)
        for pokemon in p2Update['side']['pokemon']:
            if pokemon['active']:
                hp = pokemon['condition']
                if hp == "0 fnt":
                    newHp = 0
                else:
                    newHp = int(pokemon['condition'][:pokemon['condition'].find('/')])
                p2.updatePokemonHealth(newHp)

        if forceSwitch:
            p2Switch = p2.forceSwitch(self.summary(p2))
            self.process.sendline(f">p2 switch {p2Switch.value}")
            self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")
        
        #print(p1Update)


team1 = "Lumineon||focussash|1|defog,scald,icebeam,uturn||85,85,85,85,85,85||||83|]Glaceon||lifeorb||toxic,hiddenpowerground,shadowball,icebeam||81,,85,85,85,85||,0,,,,||83|]Crabominable||choiceband|1|closecombat,earthquake,stoneedge,icehammer||85,85,85,85,85,85||||83|]Toxicroak||lifeorb|1|drainpunch,suckerpunch,gunkshot,substitute||85,85,85,85,85,85||||79|]Bouffalant||choiceband||earthquake,megahorn,headcharge,superpower||85,85,85,85,85,85||||83|]Qwilfish||blacksludge|H|thunderwave,destinybond,liquidation,painsplit||85,85,85,85,85,85||||83|"
p1 = Player("Alice", team1, "123456")
p2 = Player("Bob", team1, "123456")
test = ShowdownSimulator()
test.setup(p1, p2)
for i in range(10000):
    p1_move = p1.getMove(test.summary(p1)) 
    p2_move = p2.getMove(test.summary(p2)) 
    test.update(p1, p2)
