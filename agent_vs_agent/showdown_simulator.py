import subprocess
from random import randint
import pexpect
from player import Player
from time import sleep
from species import Species
import sys

class ShowdownSimulator():
    def __init__(self):
        self.process = pexpect.spawn('/home/wlayton/pokemon-showdown/pokemon-showdown simulate-battle',encoding='utf-8')
        self.process.logfile_read = sys.stdout
        
    def setup(self, p1, p2):
        self.process.send('>start {"formatid":"gen8ou"}\n')
        self.process.expect('update')

        self.process.send('>player p1 {"name":"%s", "team":"%s"}\n' % (p1.getName(), p1.getPackedTeam()))
        self.process.expect('update')

        self.process.sendline('>player p2 {"name":"%s", "team":"%s"}' % (p2.getName(), p2.getPackedTeam()))
        self.process.expect('update')

        self.process.sendline('>p1 team {0}'.format(p1.getOrder()))
        self.process.expect('update')

        self.process.sendline('>p2 team {0}'.format(p2.getOrder()))
        self.process.expect('update')
        
    def update(self, p1Action, p2Action):
        if p1Action > 4:
            self.process.sendline(f">p1 switch {p1Action-4}")
        else:
            self.process.sendline(f">p1 move {p1Action}")
        self.process.expect("update")

        if p2Action > 4:
            self.process.sendline(f">p2 switch {p2Action-4}")
        else:
            self.process.sendline(f">p2 move {p2Action}")
        self.process.expect("update")


team1 = "Lumineon||focussash|1|defog,scald,icebeam,uturn||85,85,85,85,85,85||||83|]Glaceon||lifeorb||toxic,hiddenpowerground,shadowball,icebeam||81,,85,85,85,85||,0,,,,||83|]Crabominable||choiceband|1|closecombat,earthquake,stoneedge,icehammer||85,85,85,85,85,85||||83|]Toxicroak||lifeorb|1|drainpunch,suckerpunch,gunkshot,substitute||85,85,85,85,85,85||||79|]Bouffalant||choiceband||earthquake,megahorn,headcharge,superpower||85,85,85,85,85,85||||83|]Qwilfish||blacksludge|H|thunderwave,destinybond,liquidation,painsplit||85,85,85,85,85,85||||83|"
p1 = Player("Alice", team1, "123456")
p2 = Player("Bob", team1, "123456")
test = ShowdownSimulator()
test.setup(p1, p2)
for i in range(10):
    p1_move = randint(1, 10)
    p2_move = randint(1, 10)
    test.update(p1_move, p2_move)

print(Species["Abra"])
print(Species(5))
