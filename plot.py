import sys
import matplotlib.pyplot as plt
import argparse
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
                # Pega as porcentagens e transforma (e.g., 0.2 -> 20%)
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


# print("\n\nY_VALUES['100%']: ", Y_VALUES['100%'])
# print("\n\nERROR['100%']: ", ERROR['100%'])


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

# # Tarjan GeeksforGeeks 100%
# plt.errorbar(
#         X_VALUES,
#         [0.023999999999999997, 0.09739999999999999, 0.2153, 0.38280000000000003,
#         0.5977, 0.8581, 1.1695, 1.5197999999999998, 1.9291999999999998, 2.3867000000000003],
#         yerr=[3.657118196434064e-18, 0.004427188724235731, 0.00377270901784558, 0.008175845182269817,
#         0.012092697520955927, 0.014433371824429058, 0.03113144176980352, 0.017008494609720464, 0.03869194575963674, 0.06583489449625725],
#         label='Tarjan GeeksforGeeks 100%',
#         # marker='o',
#         markersize=5,
#         capsize=4,
#         linewidth=2.0,
#         # lolims=True, uplims=True
#     )

# # Kosaraju GeeksforGeeks 100%
# plt.errorbar(
#         X_VALUES,
#         [0.20220000000000002, 1.0119, 2.5759, 5.3018,
#         9.5304, 14.3732, 19.5928, 30.7532, 37.8492, 52.6476],
#         yerr=[0.0013984117975601932, 0.07434820479040198, 0.01615515053748772, 0.14612232318620375,
#         0.1051107352589004, 0.22480697893476892, 0.10046867947552376, 0.7652946854353273, 0.6470404074622308, 0.7079148096895409],
#         label='Kosaraju GeeksforGeeks 100%',
#         # marker='o',
#         markersize=5,
#         capsize=4,
#         linewidth=2.0,
#         # lolims=True, uplims=True
#     )

# # Tarjan Boost 100%
# plt.errorbar(
#         X_VALUES,
#         [0.5691999999999999, 2.0233, 4.5462, 8.073599999999999, 12.610400000000002, 18.152700000000003,
#         24.6971, 32.2504, 40.803200000000004, 50.3586],
#         yerr=[0.0014757295747452452, 0.0014944341180973568, 0.0024404006956965604, 0.0036270588023296184,
#         0.004926120853842891, 0.008393780766469992, 0.013186272323055742, 0.02283369829392078, 0.024521192648176367, 0.025863745539525283],
#         label='Tarjan Boost 100%',
#         # marker='o', markersize=3,
#         capsize=4,
#         # lolims=True, uplims=True
#     )

# plt.plot(X_VALUES, [x/1000 for x in X_VALUES], label='X/1000')

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