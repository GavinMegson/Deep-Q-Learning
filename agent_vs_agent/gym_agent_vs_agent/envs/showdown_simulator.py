import pexpect
import sys
import json
from gym_agent_vs_agent.envs.player import Player
import numpy as np

class ShowdownSimulator():
    def __init__(self):
        self.process = pexpect.spawn('/home/wlayton/pokemon-showdown/pokemon-showdown simulate-battle', encoding='utf-8')
        self.process.logfile_read = sys.stdout
        #self.process.logfile = None
        self.matchOver = False

    def setup(self):
        self.primaryAgent = Player()
        self.opposingAgent = Player()

        self.process.send('>start {"formatid":"gen8ou"}\n')
        self.process.expect('update')

        teamGenerator = pexpect.spawn('/home/wlayton/pokemon-showdown/pokemon-showdown generate-team gen8ou', encoding='utf-8')
        teamGenerator.expect('\S+')
        team1 = teamGenerator.match.group(0)

        teamGenerator = pexpect.spawn('/home/wlayton/pokemon-showdown/pokemon-showdown generate-team gen8ou', encoding='utf-8')
        teamGenerator.expect('\S+')
        team2 = teamGenerator.match.group(0)

        self.process.send('>player p1 {"name":"primaryAgent", "team":"%s"}\n' % team1)
        self.process.expect('update')
        self.process.send('>player p2 {"name":"opposingAgent", "team":"%s"}\n' % team2)
        self.process.expect('update')
        self.process.send('>p1 team 123456\n')
        self.process.send('>p2 team 123456\n')

        self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")

        self.primaryAgent.update(self.process.match.group(1))
        self.opposingAgent.update(self.process.match.group(2))

    def primaryAgentReward(self):
        reward = 0
        for pokemon in self.primaryAgent.getTeam():
            if pokemon.getHp() == 0:
                reward -= 1

        for pokemon in self.opposingAgent.getTeam():
            if pokemon.getHp() == 0:
                reward += 1
        return reward

    def matchOver(self):
        return self.matchOver

    def update(self, p1Action, p2Action):
        p1Action += 1
        p1Action = self.primaryAgent.validMove(p1Action)
        if p1Action < 5:
            p1Action = ">p1 move " + str(p1Action) + "\n"
        else:
            p1Action = ">p1 switch " + str(p1Action-3) + "\n"
        p2Action = self.opposingAgent.validMove(p2Action)
        if p2Action < 5:
            p2Action = ">p2 move " + str(p2Action) + "\n"
        else:
            p2Action = ">p2 switch " + str(p2Action-3) + "\n"
        self.process.send(p1Action)
        self.process.send(p2Action)


        self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")

        self.primaryAgent.update(self.process.match.group(1))
        self.opposingAgent.update(self.process.match.group(2))

        if self.primaryAgent.forceSwitch:
            nextPokemon = self.primaryAgent.nextActivePokemon()
            self.process.send(">p1 switch " + str(nextPokemon) + "\n") 
            self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")
        if self.opposingAgent.forceSwitch:
            nextPokemon = self.opposingAgent.nextActivePokemon()
            self.process.send(">p2 switch " + str(nextPokemon) + "\n")
            self.process.expect("sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")

    def summarize(self, player):
        if player == "primary":
            return np.concatenate([self.primaryAgent.summarize()[1:], self.opposingAgent.briefSummarize()[1:]], axis=None)
        else:
            return np.concatenate([self.opposingAgent.summarize()[1:], self.primaryAgent.briefSummarize()[1:]], axis=None)

test = ShowdownSimulator()
test.setup()
print(test.summarize("primary"))
