import numpy as np
class Match():
    def __init__(player1, player2):
        self.p1 = player1
        self.p2 = player2

    def summarize(player):
        if player == self.p1.getName():
            currentPlayer = self.p1
            opponent = self.p2
        else:
            currentPlayer = self.p2
            opponent = self.p1
        summaryVector = np.array()
        for pokemon in currentPlayer.getTeam():
            summaryVector = np.concatentation(summaryVector, pokemon.summarize())
        for pokemon in opponent.getTeam():
            summaryVector = np.concatentation(summaryVector, pokemon.summarize())
        return summaryVector
