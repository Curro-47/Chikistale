import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk 
import threading
import time
import Scripts.CustomFonts as cFonts
import random
root = None
                       
globo, textoso = None, None

def _init_ (root_):
    global root, imagen_globo, globo, textoso
    root = root_

    cFonts.loadfont(b"Fonts\\DeterminationMonoWebRegular-Z5oq.ttf")
    font_determination = tkFont.Font(family="Determination Mono Web", size=18)

    imagen_globo = Image.open("Sprites\\speech_bubble.png").resize((200, 100))
    imagen_globo = ImageTk.PhotoImage(imagen_globo)

    globo = tk.Label (root, image=imagen_globo, bg='black')
    textoso = tk.Label (globo, text = "texto default", bg='white', font=font_determination, justify="left")

def spawn_bubble (texto):
    def thread ():
        time.sleep(1)

        globo.place(relx=0.62, rely=0.2, anchor="center")
        textoso.configure(text="")
        textoso.place(relx=0.2, rely=0.1)
        globo.lift()

        slowprint(texto)
        time.sleep(3)

        globo.place_forget()

    threading.Thread (target=thread, daemon=True).start()

def slowprint(texto):
    wewe= ""
    for chr in texto:
        wewe=wewe+chr
        textoso.configure(text=wewe)
        time.sleep(0.05676767)

dic = {
    "ataque": ["Hasta crees\nque con eso\nme derrotaras", "Eso no sera\nsuficiente", "Aña", "Eres debil"]
}

def dialogos(yoyoyolepareltaxiyoyoyoyoyolepareltaxi):
    random_number = random.randint(0, len(dic[yoyoyolepareltaxiyoyoyoyoyolepareltaxi]) - 1)
    coc = dic[yoyoyolepareltaxiyoyoyoyoyolepareltaxi][random_number]
    spawn_bubble(coc)