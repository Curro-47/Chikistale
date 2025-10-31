import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk 
import threading
import time
import Scripts.CustomFonts as cFonts
import random
root = None

cFonts.loadfont(b"Fonts\\DeterminationMonoWebRegular-Z5oq.ttf")
font_determination = tkFont.Font(family="Determination Mono Web", size=12)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Determination Mono Web", size=12)
                       
imagen_globo = Image.open("Sprites\\globo.png").resize((100, 100))

def _init_ (root_):
    global root 
    root = root_

globo = tk.Label (root, image = imagen_globo)
textoso = tk.Label (globo, text = "texto default")

def spawn_bubble (texto):
    def thread ():
        globo.place(relx=0.7, rely=0.4)
        textoso.configure(text="")
        textoso.place(relx=0, rely=0)
        slowprint(texto)
        time.sleep(3)
        globo.place_forget()

    threading.Thread (target=thread, daemon=True)

def slowprint(texto):
    wewe= ""
    for chr in texto:
        wewe=wewe+chr
        textoso.configure(text=wewe)
        time.sleep(0.10676767676767676767676767676767676767676767676767676767)

dic = {
    "normal": ["ingga", "polno"],
    "giganigga": ["perrita"],
}

def dialogos(yoyoyolepareltaxiyoyoyoyoyolepareltaxi):
    random_number = random.randint(0, len(dic[yoyoyolepareltaxiyoyoyoyoyolepareltaxi]-1))
    coc = dic[yoyoyolepareltaxiyoyoyoyoyolepareltaxi][random_number]
    spawn_bubble(coc)