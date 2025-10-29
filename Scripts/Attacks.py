from tkinter import *
import Scripts.TkinterShapes as ts
from PIL import Image, ImageTk
import time
import threading
import math
import random

img_spark = Image.open("Sprites\\spark.png")
img_face = Image.open("Sprites\\chikis\\boss_face.png").resize((100,100)).transpose(Image.FLIP_LEFT_RIGHT)
img_exclamation = []

attack_list = []
proyectile_list = []
attack_duration = 0

root = None
player = None
menu_size = [0, 0]
damage = None

get_scene = None

def Init(obj):
    global root, menu_size, img_spark, img_face, player, damage, get_scene
    root = obj.menu
    menu_size = [0.3*obj.screenSize[1], 0.3*obj.screenSize[1]]
    player = obj.heart
    damage = obj.Damage
    get_scene = obj.GetScene

    img_exclamation.append(ImageTk.PhotoImage(Image.open("Sprites\\exclamation0.png")))
    img_exclamation.append(ImageTk.PhotoImage(Image.open("Sprites\\exclamation1.png")))

class _Moves:
    def warning_box(self, timestamp, x0, y0, x1, y1):
        attack_list.append(Attack("warning", timestamp, Warning([x0, y0, x1, y1])))
    def warning_box_create(self, att):
        att.subclass.img = img_exclamation[0]
        att.subclass.creation_time = time.time()

        att.subclass.square = root.create_rectangle(att.subclass.pos[0]*menu_size[0], att.subclass.pos[1]*menu_size[1], att.subclass.pos[2]*menu_size[0], att.subclass.pos[3]*menu_size[1], outline='brown1', width=3)
        att.subclass.sign = root.create_image((att.subclass.pos[2]+att.subclass.pos[0])/2*menu_size[0], (att.subclass.pos[3]+att.subclass.pos[1])/2*menu_size[1], image=att.subclass.img)

        att.type = "warning0"

    def spark(self, timestamp, position, direction):
        attack_list.append(Attack("spark", timestamp, Proyectile(None, position, direction, 2)))
    def spark_create(self, att, currentTime):
        ## Rotate image based on direction
        rotation = math.degrees(math.atan2(att.subclass.dir[0], att.subclass.dir[1]))
        att.subclass.img = ImageTk.PhotoImage(img_spark.rotate(rotation))

        ## Calculate line points
        obj_position = [menu_size[0]*att.subclass.pos[0], menu_size[1]*att.subclass.pos[1]]
        largest_vector = max(abs(att.subclass.dir[0]), abs(att.subclass.dir[1]))
        obj_end_position = [obj_position[0] + att.subclass.dir[0]/largest_vector*menu_size[0]*1.5, obj_position[1] + att.subclass.dir[1]/largest_vector*menu_size[0]*1.5]

        ## Create objects
        obj = root.create_image(obj_position[0], obj_position[1], image=att.subclass.img)
        line = root.create_line(obj_position[0], obj_position[1], obj_end_position[0], obj_end_position[1], fill='gray')

        ## Add to lists
        proyectile_list.append(att.subclass)
        proyectile_list[-1].obj = obj
        proyectile_list[-1].line = line
        proyectile_list[-1].creation_time = currentTime
        attack_list.remove(att)
    
    def face(self, timestamp, position, direction, bounce, dmg=5, range=50):
        attack_list.append(Attack("face", timestamp, Face(None, position, direction, bounce)))
        attack_list[-1].subclass.dmg = dmg
        attack_list[-1].subclass.range = range
        
    def face_create(self, att, currentTime):
        att.subclass.img = ImageTk.PhotoImage(img_face.resize((att.subclass.range*2+5, att.subclass.range*2+5)))
        obj_position = [menu_size[0]*att.subclass.pos[0], menu_size[1]*att.subclass.pos[1]]
        obj = root.create_image(obj_position[0], obj_position[1], image=att.subclass.img)

        proyectile_list.append(att.subclass)
        proyectile_list[-1].obj = obj
        proyectile_list[-1].creation_time = currentTime
        attack_list.remove(att)

moves = _Moves()

class Attacks:
    def atk_facebarage(self):
        global attack_duration

        lastDir = -1
        for i in range(0, 4):
            size = [0.05, 0.5] # [to low wall, close to high wall, close to low middle, ]
            ## Choose dir
            rng = random.randint(0, 3)
            if rng == lastDir: rng = (rng + random.randint(1,3))%4
            lastDir = rng

            ## Get rectangle points
            dir = None
            if rng == 0:   dir = [size[1], size[0], 0.94-size[0], 0.94-size[0]]
            elif rng == 1: dir = [size[0], size[1], 0.94-size[0], 0.94-size[0]]
            elif rng == 2: dir = [size[0], size[0], 0.94-size[1], 0.94-size[0]]
            elif rng == 3: dir = [size[0], size[0], 0.94-size[0], 0.94-size[1]]

            moves.warning_box(i/2+1, dir[0], dir[1], dir[2], dir[3])

            if rng == 0:   dir = [1, 0]
            elif rng == 1: dir = [0, 1]
            elif rng == 2: dir = [-1, 0]
            elif rng == 3: dir = [0, -1]

            pos = None
            if dir[0] == 0: pos = [dir[1]+0.47, dir[1]/5 + 0.47] ## Down, Up
            else: pos =           [dir[0]/4 + 0.47  , dir[0]+0.47] ## Left, Right
            
            moves.face(i*0.5+3, pos, [-dir[1]*16, -dir[0]*16], 0)

        attack_duration = 7

    def atk_facebounce(self):
        global attack_duration
        face_speed = 5

        # Get direction
        degrees = random.randint(0, 3)*90 + 45 + random.randint(-20, 20)
        radians = math.radians(degrees)
        dir = [math.cos(radians) * face_speed, math.sin(radians) * face_speed]

        # Get start pos
        degrees = degrees+180 + random.randint(-20, 20)
        radians = math.radians(degrees)
        pos = [math.cos(radians), math.sin(radians)] # range (-1, 1)
        pos = [pos[0] / 2, pos[1] / 2]  # range (-0.5, 0.5)
        # Move pos to edge
        largest_vector = max(abs(pos[0]), abs(pos[1]))
        pos = [pos[0]/largest_vector, pos[1]/largest_vector]
        pos = [pos[0]+0.5, pos[1]+0.5]

        moves.face(0,pos, dir, 1)

        attack_duration = 10

    def atk_sparkgrid(self):
        global attack_duration
        spark_speed = 8

        ## Limits x=(0.075, 0.875)
        def grid(timestamp, offset):
            moves.spark(timestamp, [-0.1, (0.8 / 7) * 0 + 0.075 + offset[1]], [spark_speed,0])
            moves.spark(timestamp, [1.1, (0.8 / 7) * 2 + 0.075 + offset[1]], [-spark_speed,0])
            moves.spark(timestamp, [-0.1, (0.8 / 7) * 4 + 0.075 + offset[1]], [spark_speed,0])
            moves.spark(timestamp, [1.1, (0.8 / 7) * 6 + 0.075 + offset[1]], [-spark_speed,0])

            moves.spark(timestamp, [(0.8 / 7) * 0 + 0.075 + offset[0], -0.1], [0,spark_speed])
            moves.spark(timestamp, [(0.8 / 7) * 2 + 0.075 + offset[0], 1.1], [0,-spark_speed])
            moves.spark(timestamp, [(0.8 / 7) * 4 + 0.075 + offset[0], -0.1], [0,spark_speed])
            moves.spark(timestamp, [(0.8 / 7) * 6 + 0.075 + offset[0], 1.1], [0,-spark_speed])

        grid(1, [0,0])
        grid(2, [(0.8 / 7),(0.8 / 7)])
        grid(3, [0,0])

        attack_duration = 5
    
    def atk_sparkrandom(self):
        global attack_duration
        spark_speed = 8

        def spark(timestamp):
            # Get direction
            degrees = random.randint(1, 360)
            radians = math.radians(degrees)
            dir = [math.cos(radians) * spark_speed, math.sin(radians) * spark_speed]

            # Get start pos
            degrees = degrees+180 + random.randint(-20, 20)
            radians = math.radians(degrees)
            pos = [math.cos(radians), math.sin(radians)] # range (-1, 1)
            pos = [pos[0] / 2, pos[1] / 2]  # range (-0.5, 0.5)
            # Move pos to edge
            largest_vector = max(abs(pos[0]), abs(pos[1]))
            pos = [pos[0]/largest_vector, pos[1]/largest_vector]
            pos = [pos[0]+0.5, pos[1]+0.5]

            moves.spark(timestamp, pos, dir)
        
        for i in range(0, 15): spark(i*0.2 + 1)

        attack_duration = 6

    def atk_betray(self):
        global attack_duration, img_face
        
        moves.face(0, [-0.8, 0.5], [1, 0], 0, 999, 100)
        attack_duration = 10

def Update():
    def _Thread():
        global attack_duration
        startTime = time.time()

        while True:
            currentTime = time.time() - startTime
            plrPos = root.coords(player)
            for att in attack_list:
                if currentTime >= att.timestamp:
                    #### INSTANCE ATTACKS
                    if att.type == "spark": moves.spark_create(att, currentTime)
                    if att.type == "face": moves.face_create(att, currentTime)
                    if att.type == "warning": moves.warning_box_create(att)

                    #### Warning box
                    if att.type == "warning0":
                        blink = round(time.time()*15)%2

                        att.subclass.img = img_exclamation[blink]
                        root.itemconfigure(att.subclass.sign, image=att.subclass.img)

                        if blink==1: root.itemconfigure(att.subclass.square, outline='LightGoldenrod')
                        else: root.itemconfigure(att.subclass.square, outline='brown1')

                        if time.time() > att.subclass.creation_time + 0.5:
                            att.Delete()
                            attack_list.remove(att)

            #### PROYECTILES
            for proy in proyectile_list:
                if hasattr(proy, "creation_time") and currentTime < proy.creation_time+0.5: continue
                
                root.move(proy.obj, proy.dir[0], proy.dir[1])
                proy.pos = root.coords(proy.obj)

                distanceToPlr = max(abs(plrPos[0]-proy.pos[0]), abs(plrPos[1]-proy.pos[1]))

                if isinstance(proy, Proyectile):
                    if distanceToPlr < 18: damage(5)

                if isinstance(proy, Face): #### If proyectile is face
                    if distanceToPlr < proy.range: damage(proy.dmg)

                    ## If inside 4 bounds in order [left, right, up, down]
                    in_bounds = [proy.pos[0] >= 0, proy.pos[0] <= menu_size[0], proy.pos[1] >= 0, proy.pos[1] <= menu_size[1]]
                    
                    if proy.bounce == 1 and in_bounds == [True, True, True, True]: proy.bounce = 2

                    if proy.bounce == 2:
                        ## Clamp
                        if not in_bounds[0]: root.move(proy.obj, -proy.pos[0], 0)
                        if not in_bounds[1]: root.move(proy.obj, 0, menu_size[0]-proy.pos[0])
                        if not in_bounds[2]: root.move(proy.obj, -proy.pos[1], 0)
                        if not in_bounds[3]: root.move(proy.obj, 0, menu_size[1]-proy.pos[1])
                        ## Flip
                        if not in_bounds[0] or not in_bounds[1]: proy.dir[0] = -proy.dir[0]
                        if not in_bounds[2] or not in_bounds[3]: proy.dir[1] = -proy.dir[1]


            for proy in proyectile_list:
                ## Destoy line
                if hasattr(proy, "creation_time") and hasattr(proy, "line") and currentTime > proy.creation_time+1: 
                    root.delete(proy.line)
                if isinstance(proy, Proyectile) and currentTime > proy.creation_time+3:
                    proy.Delete()
                    proyectile_list.remove(proy)

            time.sleep(0.02)

            ## Attack end conditions
            if currentTime > attack_duration: break ## Out of time
            if get_scene() == -2: break            ## Dead
        ## Cleanup
        for proy in proyectile_list:
            proy.Delete()
        for att in attack_list:
            att.Delete()
        proyectile_list.clear()
        attack_list.clear()

    thread = threading.Thread(target=_Thread, daemon=True)
    thread.start()
    return thread

class Attack:
    type = None
    timestamp = None
    subclass = None

    def __init__(self, type, timestamp, subclass):
        self.type = type
        self.timestamp = timestamp
        self.subclass = subclass    
    
    def Delete(self):
        self.subclass.Delete()

class Proyectile:
    obj = None
    line = None
    img = None
    pos = None
    dir = None
    speed = None
    creation_time = None

    def __init__(self, obj, pos, dir, speed):
        self.obj = obj
        self.pos = pos
        self.dir = dir
        self.speed = speed
    
    def Delete(self):
        root.delete(self.obj)
        root.delete(self.line)
        del self

class Face:
    obj = None
    img = None
    pos = None
    dir = None
    bounce = None
    creation_time = None

    dmg = 5
    range = 50

    def __init__(self, obj, pos, dir, bounce):
        self.obj = obj
        self.pos = pos
        self.dir = dir
        self.bounce = bounce
    
    def Delete(self):
        root.delete(self.obj)
        del self

class Warning:
    square = None
    sign = None
    img = None
    pos = None
    creation_time = None

    def __init__(self, pos):
        self.pos = pos
    
    def Delete(self):
        root.delete(self.square)
        root.delete(self.sign)
        del self
