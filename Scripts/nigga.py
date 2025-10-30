import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk 
import threading
root = None
import Scripts.CustomFonts as cFonts
cFonts.loadfont(b"Fonts\\DeterminationMonoWebRegular-Z5oq.ttf")
font_determination = tkFont.Font(family="Determination Mono Web", size=12)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Determination Mono Web", size=12)
                       

imagen_globo = Image.open("Sprites\\globo.png").resize((100, 100))

def _init_ (root_):
    global root 
    root = root_


globo = tk.Label (root, image = imagen_globo)
textoso = tk.Label (globo, text = "texto default")


def spawn_bubble (texto):
    def thread ():
        globo.place(relx=0.7, rely=0.4)
        textoso.place(relx=0, rely=0)
    threading.Thread (target=thread, daemon=True)

