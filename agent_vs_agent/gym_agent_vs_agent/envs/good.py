import pexpect
import sys
import json
from gym_agent_vs_agent.envs.player import Player
import numpy as np
import time


class ShowdownSimulator():
    def __init__(self):
        self.process = pexpect.spawn(
            '/home/sam/dox/school/winter2021/cs510076/proj/pokemon-deep-learning/pokemon-showdown/pokemon-showdown simulate-battle', encoding='utf-8', maxread=1000000)
        # self.process.logfile_read = sys.stdout
        self.process.logfile = None
        self.matchOver = False
        #self.updates = 1
        self.switches = 1
        self.won = False

    def setup(self):
        self.primaryAgent = Player()
        self.opposingAgent = Player()

        timestr = time.strftime("%Y%m%d-%H%M%S")
        logfile = open(f'matches-rnn-c-tox/match-{timestr}.txt', 'w')
        self.process.logfile_read = logfile

        self.process.send('>start {"formatid":"gen8ou"}\n')
        self.process.expect('update')

        # tox
        team1 = "Toxapex||shedshell|regenerator|scald,knockoff,haze,recover||252,8,248,0,0,0||||82|]Hippowdon||leftovers|sandstream|stealthrock,earthquake,toxic,slackoff||252,0,4,0,252,0||||86|]Blissey||heavydutyboots|naturalcure|softboiled,teleport,seismictoss,aromatherapy||252,0,252,0,0,4||||86|]Skarmory||leftovers|sturdy|spikes,toxic,roost,bodypress||252,0,252,0,0,4|N|,0,,,,||80|]Mandibuzz||heavydutyboots|overcoat|foulplay,roost,defog,toxic||248,0,252,0,0,8|N|||84|]Slowking-Galar||assaultvest|curiousmedicine|earthquake,futuresight,sludgebomb,flamethrower||252,0,0,252,0,4||||76|"

        # test 1
        #team1 = "Claydol||leftovers|levitate|rapidspin,stealthrock,earthquake,icebeam||85,85,85,85,85,85|N|||86|]Bellossom||leftovers|chlorophyll|strengthsap,sleeppowder,gigadrain,quiverdance||85,,85,85,85,85||,0,,,,||82|]Bewear||choicescarf|fluffy|darkestlariat,doubleedge,icepunch,closecombat||85,85,85,85,85,85||||82|]Spectrier||leftovers|grimneigh|darkpulse,shadowball,substitute,nastyplot||85,,85,85,85,85|N|,0,,,,||74|]Pikachu|pikachualola|lightball|lightningrod|voltswitch,knockoff,surf,volttackle||85,85,85,85,85,85||||90|]Tapu Fini||leftovers|mistysurge|calmmind,surf,taunt,moonblast||85,,85,85,85,85|N|,0,,,,||78|"
        # test 2
        #team1 = "Vanilluxe||assaultvest|snowwarning|blizzard,freezedry,flashcannon,explosion||85,85,85,85,85,85||||82|]Stoutland||choicescarf|scrappy|wildcharge,playrough,superpower,facade||85,85,85,85,85,85||||86|]Mantine||heavydutyboots|waterabsorb|hurricane,toxic,scald,roost||85,,85,85,85,85||,0,,,,||86|]Tapu Lele||choicescarf|psychicsurge|focusblast,psyshock,shadowball,moonblast||85,,85,85,85,85|N|,0,,,,||80|]Mesprit||choicespecs|levitate|psychic,icebeam,energyball,uturn||85,85,85,85,85,85|N|||84|]Urshifu||choiceband|unseenfist|suckerpunch,ironhead,wickedblow,closecombat||85,85,85,85,85,85||||76|"

        # teamGenerator = pexpect.spawn(
        #     '/home/sam/dox/school/winter2021/cs510076/proj/pokemon-deep-learning/pokemon-showdown/pokemon-showdown generate-team gen8ou', encoding='utf-8')
        # teamGenerator.expect('\S+')
        # team1 = teamGenerator.match.group(0)
        teamGenerator = pexpect.spawn(
            '/home/sam/dox/school/winter2021/cs510076/proj/pokemon-deep-learning/pokemon-showdown/pokemon-showdown generate-team gen8ou', encoding='utf-8')
        teamGenerator.expect('\S+')
        team2 = teamGenerator.match.group(0)

        self.process.send(
            '>player p1 {"name":"primaryAgent", "team":"%s"}\n' % team1)
        self.process.expect('update')
        self.process.send(
            '>player p2 {"name":"opposingAgent", "team":"%s"}\n' % team2)
        self.process.expect('update')
        self.process.send('>p1 team 123456\n')
        self.process.send('>p2 team 123456\n')

        self.process.expect(
            "sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)")

        self.primaryAgent.update(self.process.match.group(1))
        self.opposingAgent.update(self.process.match.group(2))

    def primaryAgentReward(self):
        reward = 0
        for pokemon in self.primaryAgent.getTeam():
            if pokemon.getHp() == 0:
                reward -= 0.75

        for pokemon in self.opposingAgent.getTeam():
            if pokemon.getHp() == 0:
                reward += 2
        #reward += -0.0025 * self.updates
        reward += -0.001 * self.switches
        if self.won:
            reward += 5
        return reward

    def matchOver(self):
        return self.matchOver

    def update(self, p1Action, p2Action):
        p1Action += 1
        #self.updates += 1
        p1Action = self.primaryAgent.validMove(p1Action)
        if p1Action < 5:
            p1Action = ">p1 move " + str(p1Action) + "\n"
        else:
            self.switches += 1
            p1Action = ">p1 switch " + str(p1Action-3) + "\n"
        p2Action = self.opposingAgent.validMove(p2Action)
        if p2Action < 5:
            p2Action = ">p2 move " + str(p2Action) + "\n"
        else:
            p2Action = ">p2 switch " + str(p2Action-3) + "\n"
        #p2Action = ">p2 default\n"
        self.process.send(p1Action)
        self.process.send(p2Action)

        self.process.expect(
            "sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)|(winner)")
        if self.process.match.group(3) is not None:
            self.matchOver = True
            self.process.expect('\n')
            self.process.flush()
            self.process.close()
            return

        self.primaryAgent.update(self.process.match.group(1))
        self.opposingAgent.update(self.process.match.group(2))

        while self.primaryAgent.forceSwitch or self.opposingAgent.forceSwitch:
            if self.primaryAgent.forceSwitch:
                nextPokemon = self.primaryAgent.nextActivePokemon()
                self.process.send(">p1 switch " + str(nextPokemon) + "\n")
            if self.opposingAgent.forceSwitch:
                nextPokemon = self.opposingAgent.nextActivePokemon()
                self.process.send(">p2 switch " + str(nextPokemon) + "\n")
            self.process.expect(
                "sideupdate\r\np1\r\n(.+?}\r\n)\r\nsideupdate\r\np2\r\n(.+?}\r\n)|(winner)")
            self.primaryAgent.forceSwitch = False
            self.opposingAgent.forceSwitch = False
            if self.process.match.group(3) is not None:
                mons = 0
                for pokemon in self.primaryAgent.getTeam():
                    if pokemon.getHp() == 0:
                        mons -= 1

                for pokemon in self.opposingAgent.getTeam():
                    if pokemon.getHp() == 0:
                        mons += 1
                if mons > 0:
                    self.won = True
                self.matchOver = True
                self.process.expect('\n')
                self.process.flush()
                self.process.close()
                return
            self.primaryAgent.update(self.process.match.group(1))
            self.opposingAgent.update(self.process.match.group(2))

    def summarize(self, player):
        if player == "primary":
            return np.concatenate([self.primaryAgent.summarize()[1:], self.opposingAgent.briefSummarize()[1:]], axis=None)
        else:
            return np.concatenate([self.opposingAgent.summarize()[1:], self.primaryAgent.briefSummarize()[1:]], axis=None)

    def render(self):
        self.summarize("primary")


test = ShowdownSimulator()
test.setup()
print(test.summarize("primary"))
