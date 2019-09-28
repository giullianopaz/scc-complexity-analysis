'''
    Script para arrumar arquivo out.txt
    Em vez de salvar tempo em Milisegundos, os tempos foram salvos em microsegundos
    Este script corrige os dados e salva em fixed_out.txt
'''

from os import walk


# Pega lista de arquivos
def make_file_list(path):
      file_list = []
      for path, _, images in walk(path):
            file_list += [str(path) + '/' + elem.strip() for elem in images]
      return tuple(file_list)


FILE_LIST = make_file_list("out")

for file_name in FILE_LIST:
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            # print(file_name)
            with open('fixed_out/' + file_name.split('/')[1], 'a') as wfile:
                # print('fixed_out/' + file_name.split('/')[1])
                print('')
                print(line.strip())
                if line[0] != "#":
                    line = line.split()
                    line[2] = str(int(line[2])/1000)
                    print(' '.join(line))
                    wfile.write(' '.join(line) + '\n')
                else:
                    print(line.strip())
                    wfile.write(line)