import numpy as np
class Match():
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2

    def summarize(self, player):
        if player.getName() == self.p1.getName():
            currentPlayer = self.p1
            opponent = self.p2
        else:
            currentPlayer = self.p2
            opponent = self.p1
        summaryVector = np.empty([1,])
        for pokemon in currentPlayer.getTeam():
            summaryVector = np.concatenate((summaryVector, pokemon.summarize()))
        for pokemon in opponent.getTeam():
            summaryVector = np.concatenate((summaryVector, pokemon.summarize()))
        return summaryVector
