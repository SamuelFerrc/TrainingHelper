import math

from PIL import Image, ImageTk
import config
import os
import random

arquivo_path = os.path.join(config.output, f"treinamento_{config.index}.txt")
amostras_positivas = 0
amostras_negativas = 0
amostras_total = 0
maximo_amostras = 4096

def criar_arquivo():
    global arquivo_path

    arquivo_path = os.path.join(config.output, f"treinamento_{config.index}.txt")
    with open(arquivo_path, 'w') as arquivo:
        pass

def escrever_arquivo(conteudo):
    global arquivo_path
    arquivo_path = os.path.join(config.output, f"treinamento_{config.index}.txt")

    with open(arquivo_path, 'a') as arquivo:
        arquivo.write(conteudo)
        arquivo.write('\n')

def processar_pixel(color, distance_x, distance_y):
    global amostras_positivas, amostras_negativas, amostras_total
    if distance_x <= config.training_distance_x and distance_y <= config.training_distance_y:
        if(amostras_positivas >= maximo_amostras/2):
            return
        amostras_positivas += 1
        amostras_total +=1

    else:
        if (amostras_negativas >= maximo_amostras / 2):
            return
        amostras_negativas += 1
        amostras_total +=1
    label = "+1" if distance_x <= config.training_distance_x and distance_y <= config.training_distance_y else "-1"
    return f"{color[0]}\t{color[1]}\t{color[2]}\t{label}"
def processar_imagem(imagem: Image.Image, xD, yD):

    global amostras_positivas, amostras_negativas, amostras_total
    pixels = imagem.load()
    largura, altura = imagem.size
    print("Processando Imagem!")
    criar_arquivo()
    print(f"{altura} + {largura}")
    amostras_positivas = 0
    amostras_negativas = 0
    amostras_total = 0
    while (amostras_total < maximo_amostras):
        x = random.randint(0,largura-1)
        y = random.randint(0,altura-1)
        ##print(distancia(x,y, largura/2, altura/2))
        ##print(pixels[x,y])
        valor = processar_pixel(pixels[x,y],abs((largura/2 + xD) - x),abs((altura/2 + yD) - y))
        if valor is not None:
            escrever_arquivo(valor)

    print("Processamento Finalizado!")