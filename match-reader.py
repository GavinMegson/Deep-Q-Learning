import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from tabulate import tabulate

directory = sys.argv[1]

onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

total = 0
wins = 0
turns = 0
score = np.array([0, 0])

step_size = 100
buffer = 0
averages = []

for filename in onlyfiles:
    try:
        with open(f'{directory}/{filename}') as f:
            total += 1
            lines = f.readlines()
            data = json.loads(lines[-2])
            if data['winner'] == 'primaryAgent':
                wins += 1
                buffer += 1
            turns += data['turns']
            score += data['score']
    except:
        pass
    if total % step_size == 0:
        averages.append((total, (buffer / step_size)))
        buffer = 0

score = (score/total).round(3)
stuff = tabulate([
    ['Total Matches', total],
    ['Wins', wins],
    ['Winrate', round((wins / total), 3)],
    ['Average Turns per Match', round((turns / total), 3)],
    ['Average Alive Pokemon At End', f'{score[0]} to {score[1]}'],
    ['Sweep Factor', round(score[0] / score[1], 3)]
])

print(stuff)
a = [x[0] for x in averages]
b = [x[1] for x in averages]
plt.plot(a, b)
plt.show()
