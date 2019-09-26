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


# for label in LABELS:
#     plt.errorbar(
#         X_VALUES,
#         Y_VALUES[label],
#         yerr=ERROR[label],
#         label=label,
#         # marker='o', markersize=3,
#         capsize=4,
#         # lolims=True, uplims=True
#     )

# Tarjan GeeksforGeeks 100%
plt.errorbar(
        X_VALUES,
        [0.023999999999999997, 0.09739999999999999, 0.2153, 0.38280000000000003,
        0.5977, 0.8581, 1.1695, 1.5197999999999998, 1.9291999999999998, 2.3867000000000003],
        yerr=[3.657118196434064e-18, 0.004427188724235731, 0.00377270901784558, 0.008175845182269817,
        0.012092697520955927, 0.014433371824429058, 0.03113144176980352, 0.017008494609720464, 0.03869194575963674, 0.06583489449625725],
        label='Tarjan GeeksforGeeks 100%',
        # marker='o',
        markersize=5,
        capsize=4,
        linewidth=2.0,
        # lolims=True, uplims=True
    )

# Kosaraju GeeksforGeeks 100%
plt.errorbar(
        X_VALUES,
        [0.20220000000000002, 1.0119, 2.5759, 5.3018,
        9.5304, 14.3732, 19.5928, 30.7532, 37.8492, 52.6476],
        yerr=[0.0013984117975601932, 0.07434820479040198, 0.01615515053748772, 0.14612232318620375,
        0.1051107352589004, 0.22480697893476892, 0.10046867947552376, 0.7652946854353273, 0.6470404074622308, 0.7079148096895409],
        label='Kosaraju GeeksforGeeks 100%',
        # marker='o',
        markersize=5,
        capsize=4,
        linewidth=2.0,
        # lolims=True, uplims=True
    )

plt.plot(X_VALUES, X_VALUES, label="X")
plt.plot(X_VALUES, [elem **2 for elem in X_VALUES], label="X²")

# # Tarjan Boost 100%
# plt.errorbar(
#         X_VALUES,
#         [569.5865, 2023.8343999999997, 4546.6781, 8074.1089999999995, 12611.0346,
#         18153.350400000003, 24697.5147, 32251.019800000002, 40803.7079, 50359.1145],
#         yerr=[1.5214288057977285, 1.431809515574206, 2.3908655080906014, 3.5083472208752267,
#         4.892559911630161, 8.391533566637348, 13.156635706829618, 22.850883351756174, 24.483170797962522, 25.96754752998968],
#         label='Tarjan Boost 100%',
#         # marker='o', markersize=3,
#         capsize=4,
#         # lolims=True, uplims=True
#     )

# TODO: MUDAR NOME DO GRÁFICO
plt.title(TITLE)
# plt.ylim(bottom=1, top=5000)
plt.xlabel('Vértices')
if Y_TYPE == 'e':
    plt.ylabel('Arestas')
else:
    plt.ylabel('Tempo (s)')
plt.legend()
plt.show()