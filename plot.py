import sys
import matplotlib.pyplot as plt
from pprint import pprint

LIST = {}
FILE = sys.argv[1]

with open(FILE) as file:
    lines = file.readlines()
    for line in lines:
        label = f"{int(float(line.split()[0])*100)}%"
        try:
            LIST[label]['x'].append(int(line.split()[1]))
            LIST[label]['y'].append(int(line.split()[2]))
        except:
            LIST[label] = {
                'x': [],
                'y': []
            }
            LIST[label]['x'].append(int(line.split()[1]))
            LIST[label]['y'].append(int(line.split()[2]))
    
    pprint(LIST)

    for elem in LIST:
        plt.plot(LIST[elem]['x'], LIST[elem]['y'], label=elem, marker='o')

    # plt.plot(LIST['40%']['x'], LIST['40%']['x'], label='40%')
    

    plt.title("Título")
    plt.xlabel('Vértices')
    # plt.xticks([10,100,1000,10000])
    plt.ylabel('Tempo')
    plt.legend()
    plt.show()