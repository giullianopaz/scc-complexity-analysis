import sys
import matplotlib.pyplot as plt
import argparse
from pprint import pprint
from os import walk
from math import sqrt

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='Diretório com os dados', required=True)
parser.add_argument('--title', type=str, help='Título do gráfico')
parser.add_argument('--type', type=str, help='Tipo do gráfico (e -> Arestas | t -> tempo)')
args = parser.parse_args()

# print(args)
# exit(1)

LIST = []
PATH = args.path
X_VALUES = []
TITLE = args.title if args.title else "Título"
Y_TYPE = args.type if args.type else "t"


# Pega lista de arquivos
def make_file_list(path):
      file_list = []
      for path, _, images in walk(path):
            file_list += [str(path) + '/' + elem.strip() for elem in images]
      return tuple(file_list)


# Calcula o Desvio padrão dos dados
def get_standard_deviation(array):
    n = len(array)
    avg = sum(array)/n
    s = sum([(elem - avg)**2 for elem in array]) / (n-1)
    return sqrt(s)


# Calcula a média dos dados
def get_avg(array):
    return sum(array)/len(array)


FILE_LIST = make_file_list(PATH)
RANGE = len(FILE_LIST)
for file_name in FILE_LIST:
    files_content_list = {}
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            if line[0] != '#':
                # Pega as porcentagens e transforma (0.2 -> 20%)
                label = f"{int(float(line.split()[0])*100)}%"
                try:
                    # Lista de porcentagens
                    X_VALUES.append(int(line.split()[1]))
                    if Y_TYPE == 'e':
                        # Para pegar a quantidade de arestas
                        files_content_list[label].append(int(line.split()[3]))
                    else:
                        # Pegar o tempo em Milisegundos e divide por mil para representar em segundos
                        files_content_list[label].append(int(line.split()[2])/1000)

                    
                except:
                    files_content_list[label] = []
                    X_VALUES.append(int(line.split()[1]))
                    if Y_TYPE == 'e':
                        # Para pegar a quantidade de arestas
                        files_content_list[label].append(int(line.split()[3]))
                    else:
                        # Pegar o tempo em Milisegundos e divide por mil para representar em segundos
                        files_content_list[label].append(int(line.split()[2])/1000)

                    


    # print("\n\n", file_name)
    # pprint(files_content_list)
    LIST.append(files_content_list)

# Retira os valores repetidos e ordena
X_VALUES = sorted(set(X_VALUES))
# print("\n\nX_VALUES: ", X_VALUES)

# Retira os valores repetidos e ordena
LABELS = sorted(set([label for dict_labels in LIST for label in dict_labels.keys()]))
LABELS.append(LABELS.pop(1))
# print("\n\nLABELS: ", LABELS)

Y_VALUES = {}
for label in LABELS:
    Y_VALUES[label] = [[] for _ in range(RANGE)]

for item in LIST:
    for label, values in item.items():
        for i in range(RANGE):
            Y_VALUES[label][i].append(values[i])

ERROR = dict(Y_VALUES)

for label in LABELS:
    # Dados para o eixo Y
    Y_VALUES[label] = [get_avg(elem) for elem in Y_VALUES[label]]
    # Desvio padrão
    ERROR[label] = [get_standard_deviation(elem) for elem in ERROR[label]]

# print("\n\nY_VALUES: ", Y_VALUES)
# print("\n\nERROR: ", ERROR)

for label in LABELS:
    plt.errorbar(
        X_VALUES,
        Y_VALUES[label],
        yerr=ERROR[label],
        label=label,
        # marker='o', markersize=3,
        capsize=4,
        # lolims=True, uplims=True
    )


# TODO: MUDAR NOME DO GRÁFICO
plt.title(TITLE)
plt.xlabel('Vértices')
if Y_TYPE == 'e':
    plt.ylabel('Arestas')
else:
    plt.ylabel('Tempo (s)')
plt.legend()
plt.show()