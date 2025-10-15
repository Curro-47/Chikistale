from tkinter import *
import Scripts.TkinterShapes as ts
import math
import time
import threading

img_spark = None

attack_list = []
proyectile_list = []

root = None
menu_size = [0, 0]

def Init(_root, _menu_size):
    global root, menu_size, img_spark
    root = _root
    menu_size = _menu_size

    img_spark = PhotoImage(file="Sprites\\spark.png")

def Update():
    def _Thread():
        startTime = time.time

        while True:
            currentTime = time.time - startTime
            for att in attack_list:
                if currentTime >= att.timestamp:
                    if att.type == "spark": 
                        obj = root.create_image(menu_size[0]*att.subclass.pos[0], menu_size[1]*att.subclass.pos[1], image=img_spark)
                        proyectile_list.append(att.subclass)
                        proyectile_list[-1].obj = obj
            for proy in proyectile_list:
                root.move(proy.obj, proy.dir[0], proy.dir[1])
                proy.pos = proy.pos * proy.dir

            time.sleep(0.02)

            if currentTime > 10: break

    thread = threading.Thread(target=_Thread, daemon=True)
    thread.start()
    return thread


class _Moves:
    def spark(self, timestamp, position, direction):
        attack_list.append(Attack("spark", timestamp, Proyectile(None, position, direction, 2)))

class Attacks:
    moves = _Moves()
    
    def atk_sparkgrid(self, startTime):
        Attacks.moves.spark(0, [0,0], 0)
        Attacks.moves.spark(0, [0.5,0.5], 0)
        Attacks.moves.spark(0, [1,1], 0)

class Attack:
    type = None
    timestamp = None
    subclass = None

    def __init__(self, type, timestamp, subclass):
        self.type = type
        self.timestamp = timestamp
        self.subclass = subclass    

class Proyectile:
    obj = None
    pos = None
    dir = None
    speed = None

    def __init__(self, obj, pos, dir, speed):
        self.obj = obj
        self.pos = pos
        self.dir = dir
        self.speed = speed


