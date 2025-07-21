import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import threading
from processar_imagem import processar_imagem as pi
import config

imagem_original = None
imagem_tk = None
centro_offset_x = 0
centro_offset_y = 0

from PIL import Image, ImageTk, ImageDraw

def desenhar_imagem(offset_x=0, offset_y=0, max_largura=800, max_altura=600):
    global imagem_original, imagem_tk
    if imagem_original is None:
        return

    # Redimensiona a imagem para caber na área disponível
    imagem = imagem_original.copy()
    largura_original, altura_original = imagem.size

    # Calcula o fator de escala
    escala = min(max_largura / largura_original, max_altura / altura_original, 1.0)
    nova_largura = int(largura_original * escala)
    nova_altura = int(altura_original * escala)

    imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
    draw = ImageDraw.Draw(imagem)

    # Centro com offset
    cx = nova_largura // 2 + int(offset_x * escala)
    cy = nova_altura // 2 + int(offset_y * escala)

    # Desenha cruz
    comprimento = int(10 * escala)
    draw.line((cx, cy - comprimento, cx, cy + comprimento), fill="red", width=2)
    draw.line((cx - comprimento, cy, cx + comprimento, cy), fill="red", width=2)

    if distancefield.get() != 0 and slider_eli.get() != 0:
        raio_x = int(int(distancefield.get()) * escala)  # você pode ajustar esse valor para distorcer mais no eixo X
        raio_y = int(slider_eli.get() * escala * 0.6)  # por exemplo: 0.6 torna a elipse mais "achatada"
        bbox = (cx - raio_x, cy - raio_y, cx + raio_x, cy + raio_y)
        draw.ellipse(bbox, outline="blue", width=2)

    imagem_tk = ImageTk.PhotoImage(imagem)
    label_imagem.config(image=imagem_tk)
    label_imagem.image = imagem_tk

def abrir_imagem():
    global imagem_original
    caminho = filedialog.askopenfilename()
    if caminho:
        imagem_original = Image.open(caminho).convert("RGB")
        desenhar_imagem(centro_offset_x, centro_offset_y)

def on_slider_x(val):
    global centro_offset_x
    centro_offset_x = int(val)
    desenhar_imagem(centro_offset_x, centro_offset_y)

def on_slider_y(val):
    global centro_offset_y
    centro_offset_y = int(val)
    desenhar_imagem(centro_offset_x, centro_offset_y)

def treinar_botao():
    try:
        config.training_distance_x = int(distancefield.get())
        config.training_distance_y = int(slider_eli.get())
    except ValueError:
        print("Informe um número válido para distância!")
        return

    if imagem_original is not None:
        pi(imagem_original, slider_x.get(), slider_y.get())
    config.index += 1

def on_slider_eli(val):
    desenhar_imagem(centro_offset_x, centro_offset_y)


janela = tk.Tk()
janela.title("Visualizador de Imagens com Centro Móvel")

top_frame = tk.Frame(janela)
top_frame.pack(pady=10)

botao = tk.Button(top_frame, text="Abrir Imagem", command=abrir_imagem)
botao.grid(row=0, column=0, padx=5)

slider_x = tk.Scale(top_frame, from_=-300, to=300, orient=tk.HORIZONTAL,
                    label="Deslocamento X do Centro", command=on_slider_x, length=200)
slider_x.grid(row=0, column=1, padx=5)


slider_y = tk.Scale(top_frame, from_=-300, to=300, orient=tk.HORIZONTAL,
                    label="Deslocamento Y do Centro", command=on_slider_y, length=200)
slider_y.grid(row=0, column=2, padx=5)


slider_eli = tk.Scale(top_frame, from_=100, to=1000, orient=tk.HORIZONTAL,
                    label="Elipse Y", command=on_slider_eli, length=200)
slider_eli.grid(row=0, column=3, padx=5)



distancefield = tk.Scale(top_frame, from_=100, to=1000, orient=tk.HORIZONTAL,
                    label="Elipse X", command=on_slider_eli, length=200)
distancefield.grid(row=0, column=4, padx=5)


treinar_botao = tk.Button(top_frame, text = "Treinar", command=treinar_botao)
treinar_botao.grid(row=0, column=5, padx=5)

label_imagem = tk.Label(janela)
label_imagem.pack()

janela.mainloop()
