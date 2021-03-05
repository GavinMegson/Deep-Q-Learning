import sys
import json
from os import listdir
from os.path import isfile, join

directory = sys.argv[1]

onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

total = 0
wins = 0
turns = 0
for filename in onlyfiles:
    try:
        with open(f'{directory}/{filename}') as f:
            total += 1
            lines = f.readlines()
            data = json.loads(lines[-2])
            if data['winner'] == 'primaryAgent':
                wins += 1
            turns += data['turns']
    except:
        pass

print(f'Total: {total}')
print(f'Wins: {wins}')
print(f'Winrate: {wins/total}')
print(f'Average Turns / Match: {turns / total}')
