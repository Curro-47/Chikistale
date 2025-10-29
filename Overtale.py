from tkinter import *
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageEnhance
import math
import time
import keyboard
import threading
import random

## Local file imports
import Scripts.TkinterShapes as ts
import Scripts.Attacks as attacks
import Scripts.CustomFonts as cFonts

## Setup tkinter window
root = Tk()
root.configure(bg='black')
root.title("Overtale")
root.geometry("1280x720")
root.resizable(False, False) 
root.update()

## Import sprites and fonts
img_gameover = Image.open("Sprites\\gameover.png").convert("RGBA")
img_title = Image.open("Sprites\\title.png").convert("RGBA")

img_boss = []
img_boss.append(PhotoImage(file="Sprites\\chikis\\boss_idle.png").subsample(7, 7))
#img_boss.append(PhotoImage(file="Sprites\\placeholder.png").subsample(5, 5))
img_boss.append(PhotoImage(file="Sprites\\chikis\\boss_hit.png").subsample(4, 4))
#img_boss.append(PhotoImage(file="Sprites\\boss_damage.png").subsample(5, 5))
img_boss.append(PhotoImage(file="Sprites\\chikis\\boss_squish.png").subsample(5, 5))
img_boss.append(PhotoImage(file="Sprites\\chikis\\boss_death.png").subsample(5, 5))
img_boss.append(PhotoImage(file="Sprites\\chikis\\boss_happy.png").subsample(3, 3))
img_face = Image.open("Sprites\\chikis\\boss_face.png").resize((1000,1000)).transpose(Image.FLIP_LEFT_RIGHT)

img_heart = PhotoImage(file="Sprites\\heart.png").zoom(3, 3).subsample(2, 2)
img_heart_hurt = PhotoImage(file="Sprites\\heart_hurt.png").zoom(3, 3).subsample(2, 2)
img_heart_broken = PhotoImage(file="Sprites\\heart_broken.png").zoom(3, 3).subsample(2, 2)

img_heart_shard = []
img_heart_shard.append(PhotoImage(file="Sprites\\heart_shard0.png").zoom(2, 2))
img_heart_shard.append(PhotoImage(file="Sprites\\heart_shard1.png").zoom(2, 2))
img_heart_shard.append(PhotoImage(file="Sprites\\heart_shard2.png").zoom(2, 2))
img_heart_shard.append(PhotoImage(file="Sprites\\heart_shard1.png").zoom(2, 2))

img_buttons = PhotoImage(file="Sprites\\battle_buttons.png")
img_hp = PhotoImage(file="Sprites\\hp.png")
img_target = PhotoImage(file="Sprites\\target.png").zoom(3,3).subsample(2,2)
img_target_aim = PhotoImage(file="Sprites\\target_aim.png").zoom(3,3).subsample(2,2)
img_target_aim2 = PhotoImage(file="Sprites\\target_aim2.png").zoom(3,3).subsample(2,2)

img_text = PhotoImage(file="Sprites\\text.png")

root.iconphoto(True, img_heart)

cFonts.loadfont(b"Fonts\\DeterminationMonoWebRegular-Z5oq.ttf")
font_determination = tkFont.Font(family="Determination Mono Web", size=12)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Determination Mono Web", size=12)

class Objects:
    def GetScene(self): ## Get the current obj.scene, used in other files
        return self.scene

    def Dialogue(self, txt, place=True):
        self.menu_dialogue.configure(text = "")

        if place:
            thread = ts.Resize(self.menu_border, subObject=self.menu, w=0.67, h=0.3)
            self.menuSize = (0.67, 0.3)
            self.menu_dialogue.place(x=20, y=20)

            thread.join()

        txtNew = ""
        
        obj.pressed_space = False
        for chr in txt:
            if chr == '@':
                time.sleep(0.1)
                continue
            txtNew = txtNew + chr
            self.menu_dialogue.configure(text=txtNew)
            
            if not obj.pressed_space: time.sleep(0.05)

    def Damage(self, dmg):
        if time.time() < self.immunity_until: return

        self.health -= dmg

        self.immunity_until = time.time() + 0.5

        if self.health > self.max_health: 
            self.health = self.max_health
        elif self.health <= 0:
            self.health = 0
            self.scene = -2
        
        healthDisplay = str(self.health).zfill(2)+"/"+str(self.max_health).zfill(2)
        self.info_hp_display.configure(text=healthDisplay)

        self.info_hp_bar.place_configure(width=0.05*self.screenSize[0]*(self.health/self.max_health))

    def DamageBoss(self, dmg):
        def _thread():
            nonlocal dmg

            if obj.trust_level >= 99: dmg = 999

            startBossHealth = self.boss_health

            self.boss_health_base.place(x=0.5*self.screenSize[0], y=0.15*self.screenSize[1], width=0.15*self.screenSize[0], height=0.04*self.screenSize[1], anchor=CENTER)

            ## Place damage numbers
            dmg = min(dmg, 99)
            self.boss_damage_number0.place(x=0.48*self.screenSize[0], y=0.09*self.screenSize[1], width=0.0457*self.screenSize[0], height=0.0457*self.screenSize[0], anchor=CENTER)
            if dmg>=10: self.boss_damage_number1.place(x=0.52*self.screenSize[0], y=0.09*self.screenSize[1], width=0.0457*self.screenSize[0], height=0.0457*self.screenSize[0], anchor=CENTER)
            
            self.bdn0.place_configure(x=cFonts.char(int(str(dmg)[0]))[0]*0.0457*self.screenSize[0])
            if dmg>=10: self.bdn1.place_configure(x=cFonts.char(int(str(dmg)[1]))[0]*0.0457*self.screenSize[0])
            
            if dmg<10: self.boss_damage_number0.place_configure(x=0.5*self.screenSize[0])

            if dmg == 99: dmg = 999

            ## Animation
            ## Death condition
            if startBossHealth - dmg <= 0: 
                self.scene = -3
                self.boss_img.configure(image=img_boss[2])
            else:
                if obj.trust_level>=0: obj.trust_level -= 1
                self.boss_img.configure(image=img_boss[1])

            loopStartGlobalTime = time.time()
            while True:
                loopTime = time.time() - loopStartGlobalTime
                if loopTime > 1: break

                self.boss_health = startBossHealth - (dmg*loopTime)

                self.boss_health_bar.update()
                self.boss_health_bar.place_configure(width=(0.15*self.screenSize[0]*(self.boss_health/self.boss_max_health)))

                ## Shake animation
                shake = math.sin(loopTime*40)*20 * (1-loopTime)
                shake = math.tanh(8 * math.sin(loopTime*40))*20 * (1-loopTime)

                self.boss.place_configure(x=0.5*self.screenSize[0]+shake, anchor=CENTER)

                ## Number animation
                jump = math.sin(loopTime/0.75 * math.pi)*25
                if loopTime > 0.75: jump = 0

                self.boss_damage_number0.place_configure(y=0.09*self.screenSize[1] - jump)
                self.boss_damage_number1.place_configure(y=0.09*self.screenSize[1] - jump)

                time.sleep(0.02)

            time.sleep(0.5)

            if startBossHealth - dmg > 0: self.boss_img.configure(image=img_boss[0])

            self.boss_health_base.place_forget()
            self.boss_damage_number0.place_forget()
            self.boss_damage_number1.place_forget()

        thread = threading.Thread(target=_thread, daemon=True)
        thread.start()
        return thread

    def __init__(self):
        ## Prepare variables
        self.scene = -1 # 0 menu, 1 battle, 2 attack, 3 act, 4 item, 5 mercy
        self.selectedButton = 0
        self.trust_level = 0
        self.lastAttack = None
        self.attackThread = None

        ## Customization
        self.menuSize = (0.7, 0.3)
        self.screenSize = (1280, 720)
        self.lineWidth = self.screenSize[0]/100

        if not hasattr(self, "max_health"): self.max_health = 20
        self.health = self.max_health
        self.max_damage = 16
        self.immunity_until = 0

        self.used_chikiramen = False
        self.pressed_space = False
        self.spare_condition = False

        self.boss_max_health = 100
        self.boss_health = self.boss_max_health

        ts.Init(self.screenSize, self.lineWidth)

        ## Create objects
        self.boss, self.boss_img = ts.ImageSquare(root, x=0.5, y=0.35, w=0.2, rh=1.08, image=img_boss[0], offset=(0.5, 0.5))
        self.menu, self.menu_border = ts.Square(root, x=0.5, y=0.65, w=self.menuSize[0], h=self.menuSize[1])
        self.menu_dialogue = Label(self.menu, text="None", bg='black', fg='white', justify="left")
        self.heart = self.menu.create_image(self.menuSize[0]*self.screenSize[0]/2, self.menuSize[1]*self.screenSize[1]/2, image=img_heart)
        self.heart_menu, self.heart_menu_img = ts.ImageSquare(root, image=img_heart, x=0.5, y=0.5, w=40, rh=1, relative=False, image_anchor="nw")
        self.heart_menu.place_forget()

        self.debug = Label(root, text="Debug")
        self.debug.place(x=0, y=0)

        self.info_name = ts.TextSquare(root, text="CURRO  LV 1", size=30, x=0.25, y=0.875, anchor="sw")
        self.info_hp_text, _ = ts.ImageSquare(root, x=0.45, y=0.865, w=0.05, rh=0.5, image=img_hp, offset=(0.5, 0.5), anchor="sw", image_anchor=CENTER)
        self.info_hp_frame = ts.FillSquare(root, x=0.50, y=0.87, w=0.049, h=0.05, bg='red3', anchor="sw")
        self.info_hp_bar = ts.FillSquare(self.info_hp_frame, x=-0.001, y=0, w=0.05, h=0.05, bg='yellow', anchor="nw")
        self.info_hp_display = ts.TextSquare(root, text=str(self.health)+"/"+str(self.max_health), size=30, x=0.56, y=0.875, anchor="sw")

        self.button_fight, self.button_fight_image = ts.ImageSquare(root, image=img_buttons, x=0.2, y=0.88, w=170, h=70, relative=False, anchor="nw", image_anchor="nw", offset=(0,0))
        self.button_act, self.button_act_image = ts.ImageSquare(root, image=img_buttons, x=0.36, y=0.88, w=170, h=70, relative=False, anchor="nw", image_anchor="nw", offset=(-1.05,0))
        self.button_item, self.button_item_image = ts.ImageSquare(root, image=img_buttons, x=0.64, y=0.88, w=170, h=70, relative=False, anchor="ne", image_anchor="nw", offset=(-2.1,0))
        self.button_mercy, self.button_mercy_image = ts.ImageSquare(root, image=img_buttons, x=0.8, y=0.88, w=170, h=70, relative=False, anchor="ne", image_anchor="nw", offset=(-3.15,0))

        self.attack_menu = Canvas(self.menu, bg='black')
        self.attack_target = self.attack_menu.create_image(self.screenSize[0]*self.menuSize[0]/2-self.screenSize[0]/100, self.screenSize[1]*self.menuSize[1]/2+self.screenSize[0]/200, image=img_target)
        self.attack_aim = self.attack_menu.create_image(0, self.screenSize[1]*self.menuSize[1]/2+self.screenSize[0]/200, image=img_target_aim)

        self.boss_health_base = ts.FillSquare(root, x=0.5, y=0.15, w=0.15, h=0.04, bg='gray26')
        self.boss_health_bar = ts.FillSquare(self.boss_health_base, x=0, y=0, w=0.15, h=0.04, bg='green3', anchor="nw")
        self.boss_damage_number0, self.bdn0 = ts.ImageSquare(root, x=0.48, y=0.09, w=0.0457, rh=1, image=img_text, image_anchor="nw", offset=cFonts.char(8))
        self.boss_damage_number1, self.bdn1 = ts.ImageSquare(root, x=0.52, y=0.09, w=0.0457, rh=1, image=img_text, image_anchor="nw", offset=cFonts.char(7))

        self.boss_health_base.place_forget()
        self.boss_damage_number0.place_forget()
        self.boss_damage_number1.place_forget()

        self.display_text = Label(self.menu, text="* Chiki-ramen", bg='black', fg='white', justify="left")

        self.atk = attacks.Attacks()
        attacks.Init(self)

    def clear(self, exceptions = []):
        menuOffset = [(0.5 - self.menuSize[0]/2) * self.screenSize[0] + 7, (0.65 - self.menuSize[1]/2) * self.screenSize[1] + 7]

        ## Blacken Menu and make it fill the screen
        self.menu.place_configure(width=self.screenSize[0], height=self.screenSize[1], x = 0, y = 0, anchor="nw")
        self.menu_border.place_configure(width=self.screenSize[0], height=self.screenSize[1], x = 0, y = 0, anchor="nw")
        self.menu.configure(highlightthickness=0)
        self.menu_border.configure(bg='black', highlightthickness=0)

        if "heart" in exceptions:
            ## Recenter heart
            self.menu.move(self.heart, menuOffset[0], menuOffset[1])
        else:
            self.menu.delete(self.heart)

        ## Delete everything else
        if not "boss" in exceptions: 
            self.boss.destroy()
        else: 
            self.boss.lift()

        self.info_hp_bar.destroy()
        self.info_hp_display.destroy()
        self.info_hp_frame.destroy()
        self.info_hp_text.destroy()
        self.info_name.destroy()
        self.button_fight.destroy()
        self.button_item.destroy()
        self.button_act.destroy()
        self.button_mercy.destroy()
        self.display_text.destroy()

        self.heart_menu.place_forget()

        del self


obj = None

def Keybind(bind):
    binds = {
        "up": ["up", "w"],
        "down": ["down", "s"],
        "left": ["left", "a"],
        "right": ["right", "d"],
        "select": ["space", "enter", "z"]
    }

    return any(keyboard.is_pressed(k) for k in binds[bind])

def Thread():
    def _thread():
        global obj
        while True:
            if obj!= None: obj.debug.configure(text="Scene "+str(obj.scene))
            #### STARTUP
            if obj == None or obj.scene == -1:
                obj = Objects()
                obj.clear()
                time.sleep(1)

                tk_img0 = ImageTk.PhotoImage(img_title)
                title = obj.menu.create_image(obj.screenSize[0]/2, obj.screenSize[1]/2, image=tk_img0)

                enhancer = ImageEnhance.Brightness(img_face)
                darker_img = enhancer.enhance(0)
                tk_img1 = ImageTk.PhotoImage(darker_img)

                face = obj.menu.create_image(obj.screenSize[0]/2, obj.screenSize[1]/2, image=tk_img1)
                obj.menu.tag_raise(title)

                startTime = time.time()
                animDuration = 4
                
                obj.pressed_space = False
                while True:
                    currentTime = time.time() - startTime
                    if obj.pressed_space: currentTime = animDuration

                    darker_img = enhancer.enhance(currentTime / animDuration *0.2)
                    tk_img1 = ImageTk.PhotoImage(darker_img)
                    obj.menu.itemconfigure(face, image=tk_img1)

                    obj.menu.image_ref = tk_img1

                    if currentTime >= animDuration: break
                    time.sleep(0.05)

                text = Label(root, text="[ PRESS SPACE TO START ]", bg='black', fg='yellow')
                text.place(relx=0.5, rely=0.8, anchor=CENTER)

                while not obj.pressed_space: time.sleep(0.1)
                obj.pressed_space = False

                text.destroy()
                button0 = Label(root, text="Easy", bg='black', fg='white')
                button1 = Label(root, text="Medium", bg='black', fg='white')
                button2 = Label(root, text="Hard", bg='black', fg='white')
                button0.place(relx=0.3, rely=0.8, anchor=CENTER)
                button1.place(relx=0.5, rely=0.8, anchor=CENTER)
                button2.place(relx=0.7, rely=0.8, anchor=CENTER)

                selectedButton = 0
                def _update():
                        nonlocal selectedButton
                        selectedButton = selectedButton%3
                        if selectedButton == 0: 
                            button0.configure(fg='yellow')
                            button1.configure(fg='white')
                            button2.configure(fg='white')
                        elif selectedButton == 1: 
                            button0.configure(fg='white')
                            button1.configure(fg='yellow')
                            button2.configure(fg='white')
                        elif selectedButton == 2: 
                            button0.configure(fg='white')
                            button1.configure(fg='white')
                            button2.configure(fg='yellow')
                _update()
                while not obj.pressed_space: 
                    if Keybind("left"): 
                        selectedButton += -1
                        _update()
                    if Keybind("right"): 
                        selectedButton += 1
                        _update()
                    
                    while Keybind("left") or Keybind("right"): time.sleep(0.05)
                    
                    time.sleep(0.02)
                obj.pressed_space = False

                if selectedButton == 0: obj.max_health = 80
                elif selectedButton == 1: obj.max_health = 20
                elif selectedButton == 2: obj.max_health = 1
                obj.health = obj.max_health

                button0.destroy()
                button1.destroy()
                button2.destroy()
                obj.menu.delete(title)
                obj.menu.delete(face)

                obj.__init__()
                obj.selectedButton =-1
                UpdateSelectedButton()
                
                obj.scene = 0
            
            #### DEATH SCENE
            elif obj.scene == -2:
                obj.selectedButton =-1
                UpdateSelectedButton()

                menuOffset = [(0.5 - obj.menuSize[0]/2) * obj.screenSize[0] + 7, (0.65 - obj.menuSize[1]/2) * obj.screenSize[1] + 7]
                heartPos = obj.menu.coords(obj.heart)
                heartPos = [heartPos[0] + menuOffset[0], heartPos[1] + menuOffset[1]]

                obj.clear(["heart"])

                ## Invisible gameover screen
                gameover = obj.menu.create_image(obj.screenSize[0]/2, obj.screenSize[1]*0.2)

                ## Heart break
                time.sleep(0.3)
                obj.menu.itemconfigure(obj.heart, image=img_heart_broken)

                ## Heart explode
                time.sleep(1.5)
                obj.menu.delete(obj.heart)
                heart_shards = []
                for i in range(6):
                    shard = obj.menu.create_image(heartPos[0], heartPos[1])
                    shard_speed = 5

                    # Get direction
                    degrees = i/6*360 + random.randint(-60, 60)
                    radians = math.radians(degrees)
                    dir = [math.cos(radians) * shard_speed, math.sin(radians) * shard_speed]

                    heart_shards.append([shard, dir])

                startTime = time.time()
                lastUpdate = startTime
                while startTime > time.time() - 4:
                    #### HEART SHARDS
                    for shard in heart_shards:
                        ## Movement
                        obj.menu.move(shard[0], shard[1][0], shard[1][1])
                        shard[1] = [shard[1][0], shard[1][1]+0.15]

                        ## Animation
                        frame = math.floor((time.time() % 0.4) / 0.4 * len(img_heart_shard))
                        obj.menu.itemconfigure(shard[0], image=img_heart_shard[frame])

                    #### GAME OVER TEXT
                    if startTime + 2 < time.time():
                        # Set image darkness
                        darkness = min((time.time() - startTime - 2) / 2, 1)
                        enhancer = ImageEnhance.Brightness(img_gameover)
                        darker_img = enhancer.enhance(darkness)

                        ## Add Image
                        tk_img = ImageTk.PhotoImage(darker_img)
                        obj.menu.itemconfigure(gameover, image=tk_img)

                        obj.menu.image_ref = tk_img

                        lastUpdate = time.time()
                    time.sleep(0.02)

                obj.menu_dialogue.place(x=obj.screenSize[0]*0.5, y=obj.screenSize[1]*0.65, anchor=CENTER)
                obj.Dialogue("No te rindas ahora @@@@@.@@@@@.@@@@@.@@@@@@@@@@\n  Ten DETERMINACION", False)

                time.sleep(3)

                obj.Dialogue("* Intentar de nuevo\n\n* Rendirse  ", False)

                obj.heart_menu_img.configure(image= img_heart_broken)
                obj.heart_menu.place(x=0.305*obj.screenSize[0], y=0.5*obj.screenSize[1], width=35, height=29)
                selectedMenuButton = 0
                obj.pressed_space = False
                
                while obj.scene == -2:
                    if Keybind("up"): selectedMenuButton = 0
                    if Keybind("down"): selectedMenuButton = 1
                    
                    if selectedMenuButton == 0:
                        obj.heart_menu.place_configure(y=0.575*obj.screenSize[1])
                    if selectedMenuButton == 1:
                        obj.heart_menu.place_configure(y=0.69*obj.screenSize[1])
                    if obj.pressed_space: 
                        if selectedMenuButton == 1: on_close()
                        break
                    time.sleep(0.02)
                obj.pressed_space = False

                obj.heart_menu.place_forget()
                obj.menu_dialogue.destroy()
                obj.menu.delete(gameover)

                obj.scene = -1
            
            #### ENDINGS
            elif obj.scene == -3:
                obj.selectedButton =-1
                UpdateSelectedButton()

                obj.clear(["boss"])

                if obj.boss_health <=0 and obj.trust_level >= 99: 
                    txt = "Final malo verdadero:@@@@@@@@@@\nLa traicion @@@@@.@@@@@.@@@@@.@@@@@ Eres un monstruo"
                    obj.boss_img.configure(image=img_boss[3])
                elif obj.boss_health <=0: 
                    txt = "Final malo:@@@@@@@@@@\nGanaste @@@@@.@@@@@.@@@@@.@@@@@ Pero a que costo"
                    obj.boss_img.configure(image=img_boss[3])
                elif obj.boss_health <=obj.max_damage: txt = "Final neutro:@@@@@@@@@@\nChikis A HUIDO @@@@@.@@@@@.@@@@@.@@@@@ Al menos ambos siguen vivos"
                elif obj.trust_level == 999: 
                    txt = "Final bueno:@@@@@@@@@@\nChikis come el chiki-ramen @@@@@.@@@@@.@@@@@.@@@@@ Le encanto"
                    obj.boss_img.configure(image=img_boss[4])
                else: txt = "Error:@@@@@@@@@@\nNo se encontro el final"

                time.sleep(1)

                obj.menu_dialogue.place(x=obj.screenSize[0]*0.5, y=obj.screenSize[1]*0.7, anchor=CENTER)
                obj.menu_dialogue.configure(justify="center")

                txt = txt + "@@@@@@@@@@@@@@@@@@@@\n\n* Jugar de nuevo \n\n* Cerrar el juego"

                obj.Dialogue(txt, False)

                #### Button select
                obj.heart_menu.place(x=0.33*obj.screenSize[0], y=0.5*obj.screenSize[1], width=29, height=29)
                selectedMenuButton = 0
                obj.pressed_space = False
                
                while obj.scene == -3:
                    if Keybind("up"): selectedMenuButton = 0
                    if Keybind("down"): selectedMenuButton = 1
                    
                    if selectedMenuButton == 0:
                        obj.heart_menu.place_configure(y=0.712*obj.screenSize[1])
                    if selectedMenuButton == 1:
                        obj.heart_menu.place_configure(y=0.827*obj.screenSize[1])
                    if obj.pressed_space: 
                        if selectedMenuButton == 1: on_close()
                        break
                    time.sleep(0.02)
                obj.pressed_space = False

                obj.menu_dialogue.destroy()
                
                obj.scene = -1




            #### NOT FIGHTMODE (Menu)
            elif obj.scene == 0:
                thread = ts.Resize(obj.menu_border, subObject=obj.menu, w=0.67, h=0.3)
                obj.menuSize = (0.67, 0.3)

                obj.selectedButton =-1
                heartPos = obj.menu.coords(obj.heart)
                obj.menu.move(obj.heart, -heartPos[0]-40, -heartPos[1]-40)

                thread.join()
                obj.selectedButton =0
                UpdateSelectedButton()

                obj.display_text.configure(text="* Chikis")
                obj.display_text.place(x=80, y=30, anchor="nw")
                obj.menu_dialogue.lift()

                while obj.scene == 0: time.sleep(0.1)

                obj.menu_dialogue.place_forget()
                obj.display_text.place_forget()
                obj.heart_menu.place_forget()
            
            #### FIGHTMODE
            elif obj.scene == 1:
                thread = ts.Resize(obj.menu_border, subObject=obj.menu, w=0.3/obj.screenSize[0]*obj.screenSize[1], h=0.3)
                obj.selectedButton =-1
                UpdateSelectedButton()
                obj.menuSize = (0.3/obj.screenSize[0]*obj.screenSize[1], 0.3)
                thread.join()

                heartPos = obj.menu.coords(obj.heart)
                obj.menu.move(obj.heart, -heartPos[0]+obj.screenSize[0]*obj.menuSize[0]/2 -3, -heartPos[1]+obj.screenSize[1]*obj.menuSize[1]/2 -3)
                
                #### Choose attack
                rng = random.randint(0, 3)
                if rng == obj.lastAttack: rng = (random.randint(1, 3)+1)%3
                obj.lastAttack = rng
                if obj.trust_level <= -99: rng = -1

                if rng==0: obj.atk.atk_sparkrandom()
                elif rng==1: obj.atk.atk_sparkgrid()
                elif rng==2: obj.atk.atk_facebounce()
                elif rng==3: obj.atk.atk_facebarage()
                elif rng==-1: obj.atk.atk_betray()


                obj.attackThread = attacks.Update()
                
                while obj.scene == 1:
                    obj.menu.tag_raise(obj.heart)

                    immunity_time = obj.immunity_until+0.5 - time.time()
                    if immunity_time > 0:
                        blinking = math.floor(immunity_time * 10) % 2

                        if blinking == 0: obj.menu.itemconfig(obj.heart, image=img_heart)
                        if blinking == 1: obj.menu.itemconfig(obj.heart, image=img_heart_hurt)

                    heartPos = obj.menu.coords(obj.heart)
                    ## Movement
                    speed = 4

                    move = [0, 0]
                    if Keybind("left"): move[0] += -speed
                    if Keybind("right"): move[0] += speed
                    if Keybind("up"): move[1] += -speed
                    if Keybind("down"): move[1] += speed

                    ## offsetLeft, offsetUp, offsetRight, offsetDown
                    offset = [heartPos[0]+move[0]-15, heartPos[1]+move[1]-15, (obj.menuSize[0]*obj.screenSize[0])-heartPos[0]-move[0]-30, (obj.menuSize[1]*obj.screenSize[1])-heartPos[1]-move[1]-30]
                    
                    ## Collision with borders
                    if offset[0] < 0: move[0] = 0
                    if offset[1] < 0: move[1] = 0
                    if offset[2] < 0: move[0] = 0
                    if offset[3] < 0: move[1] = 0

                    obj.menu.move(obj.heart, move[0], move[1])

                    if not obj.attackThread.is_alive(): obj.scene = 0

                    time.sleep(0.02)
            
            ## Attack scene
            elif obj.scene == 2:
                thread = ts.Resize(obj.menu_border, subObject=obj.menu, w=0.67, h=0.3)
                obj.menuSize = (0.67, 0.3)
                thread.join()

                obj.attack_menu.place(x=-obj.screenSize[0]/100, y=-obj.screenSize[0]/100, width = obj.screenSize[0]*obj.menuSize[0]+obj.screenSize[0]/100, height = obj.screenSize[1]*obj.menuSize[1]+obj.screenSize[0]/100, anchor="nw")
                attack_aim = obj.attack_menu.create_image(0, obj.screenSize[1]*obj.menuSize[1]/2+obj.screenSize[0]/200, image=img_target_aim)

                obj.selectedButton =-1
                UpdateSelectedButton()


                attackStartGlobalTime = time.time()
                while obj.scene == 2:
                    attackTime = time.time() - attackStartGlobalTime
                    if attackTime < 0.5: continue

                    obj.attack_menu.move(attack_aim, 12, 0)
                    if Keybind("select"): break
                    if attackTime > 2.2: break

                    time.sleep(0.02)

                attackStartGlobalTime = time.time()
                
                def AnimAim():
                    attackTime = time.time() - attackStartGlobalTime
                    while attackTime < 0.75:
                        attackTime = time.time() - attackStartGlobalTime

                        obj.attack_menu.itemconfigure(attack_aim, image=img_target_aim2)
                        time.sleep(0.08)
                        obj.attack_menu.itemconfigure(attack_aim, image=img_target_aim)
                        time.sleep(0.08)
                    obj.attack_menu.delete(attack_aim)
                    obj.attack_menu.place_forget()
                anim_aim = threading.Thread(target=AnimAim, daemon=True)
                anim_aim.start()

                time.sleep(0.5)

                # Calculate damage
                dmg = round((435.75 - abs(436 - obj.attack_menu.coords(attack_aim)[0]))/436 * obj.max_damage)
                if dmg < 0: dmg = 0
                anim_dmgboss = obj.DamageBoss(dmg)

                anim_aim.join()
                anim_dmgboss.join()

                if obj.boss_health < obj.max_damage: obj.spare_condition = True
                if obj.scene != -3: obj.scene = 1

            ## Act obj.scene
            elif obj.scene == 3:
                obj.selectedButton =-1
                UpdateSelectedButton()

                obj.display_text.place(x=80, y=30, anchor="nw")
                obj.display_text.configure(text="* Inspeccionar     * Insultar\n* Convencer        * Regresar")
                obj.heart_menu.place(x=0.2*obj.screenSize[0], y=0.565*obj.screenSize[1], width=29, height=29)

                selectedMenuButton = [0, 0]
                obj.pressed_space = False
                while obj.scene == 3:
                    if Keybind("left"): selectedMenuButton[0] = 0
                    if Keybind("right"): selectedMenuButton[0] = 1
                    if Keybind("up"): selectedMenuButton[1] = 0
                    if Keybind("down"): selectedMenuButton[1] = 1
                    
                    if selectedMenuButton == [0,0]: obj.heart_menu.place_configure(x=0.2*obj.screenSize[0], y=0.565*obj.screenSize[1])
                    if selectedMenuButton == [0,1]: obj.heart_menu.place_configure(x=0.2*obj.screenSize[0], y=0.622*obj.screenSize[1])
                    if selectedMenuButton == [1,0]: obj.heart_menu.place_configure(x=0.5*obj.screenSize[0], y=0.565*obj.screenSize[1])
                    if selectedMenuButton == [1,1]: obj.heart_menu.place_configure(x=0.5*obj.screenSize[0], y=0.622*obj.screenSize[1])

                    if obj.pressed_space: break
                obj.pressed_space = False

                obj.display_text.place_forget()
                obj.heart_menu.place_forget()

                if selectedMenuButton == [0, 0]:
                    obj.Dialogue("* Chikis - ATK 5 DEF 100\n* Le gusta el ramen")

                    obj.scene = 0
                elif selectedMenuButton == [0, 1]:
                    txt = ["* Pides piedad a Chikis\n* Te mira friamente",
                           "* Le pides a Chikis \n  que reconsidere\n* No parece contestar",
                           "* Le dices a Chikis que \n  el no es asi\n* Parece que lo piensa un poco",
                           "* Tratas de convencer a Chikis\n* Lo esta considerando",
                           "* Le pides unas ultimas disculpas a \n  Chikis\n* Parece a punto de aceptar\n* Tal vez un regalo podria ayudar",
                           "***",
                           "* Le pides disculpas a Chikis\n* Te mira con odio"]
                    
                    obj.Dialogue(txt[obj.trust_level])

                    time.sleep(2)
                    obj.menu_dialogue.place_forget()

                    obj.trust_level = min(obj.trust_level+1, 5)
                    if obj.trust_level >= 5: obj.spare_condition = True
                    obj.scene = 1
                elif selectedMenuButton == [1, 0]:
                    obj.Dialogue("* Insultas a Chikis\n* Se ve mas enojado?")

                    time.sleep(2)
                    obj.menu_dialogue.place_forget()

                    obj.trust_level = max(obj.trust_level-1, -5)
                    obj.scene = 1
                elif selectedMenuButton == [1, 1]:
                    obj.scene = 0

            ## Items obj.scene
            elif obj.scene == 4:
                obj.selectedButton =-1
                UpdateSelectedButton()

                obj.display_text.place(x=80, y=30, anchor="nw")
                obj.heart_menu.place(x=0.2*obj.screenSize[0], y=0.565*obj.screenSize[1], width=29, height=29)

                if (obj.used_chikiramen):
                    obj.display_text.configure(text="* Regresar\n\nNo tienes objetos")

                    while Keybind("select"): time.sleep(0.02)
                    while not Keybind("select"): time.sleep(0.02)

                    obj.display_text.place_forget()
                    obj.heart_menu.place_forget()

                    obj.scene = 0
                else:
                    obj.display_text.configure(text="* Chiki-ramen\n* Regresar")

                    selectedMenuButton = 0
                    while obj.scene == 4:
                        if Keybind("up"): selectedMenuButton = 0
                        if Keybind("down"): selectedMenuButton = 1
                        
                        if selectedMenuButton == 0:
                            obj.heart_menu.place_configure(y=0.565*obj.screenSize[1])
                        if selectedMenuButton == 1:
                            obj.heart_menu.place_configure(y=0.622*obj.screenSize[1])
                        if obj.pressed_space: break
                    obj.pressed_space = False

                    obj.display_text.place_forget()
                    obj.heart_menu.place_forget()

                    if selectedMenuButton == 0:
                        gave_chiki_ramen = False
                        if obj.trust_level >= 5:
                            obj.display_text.configure(text="* Comer\n* Dar a Chikis")
                            obj.display_text.place(x=80, y=30, anchor="nw")
                            obj.heart_menu.place(x=0.2*obj.screenSize[0], y=0.565*obj.screenSize[1], width=29, height=29)

                            selectedMenuButton = 0
                            while obj.scene == 4:
                                if Keybind("up"): selectedMenuButton = 0
                                if Keybind("down"): selectedMenuButton = 1
                                
                                if selectedMenuButton == 0:
                                    obj.heart_menu.place_configure(y=0.565*obj.screenSize[1])
                                if selectedMenuButton == 1:
                                    obj.heart_menu.place_configure(y=0.622*obj.screenSize[1])
                                if obj.pressed_space: break
                            obj.pressed_space = False

                            if selectedMenuButton == 1: 
                                gave_chiki_ramen = True

                                obj.display_text.place_forget()
                                obj.heart_menu.place_forget()
                                obj.Dialogue("* Chikis devora el ramen\n* Ya no quiere pelear")

                                obj.trust_level = 999
                                obj.scene = 0

                        #### HEAL
                        if not gave_chiki_ramen:
                            obj.Damage(-20)

                            obj.display_text.place_forget()
                            obj.heart_menu.place_forget()

                            obj.Dialogue("* Comiste el Chiki-Ramen")
                            time.sleep(2)

                            obj.menu_dialogue.place_forget()
                            obj.used_chikiramen = True

                            obj.scene = 1
                    else:
                        obj.scene = 0
                obj.pressed_space = False

            ## Mercy scene
            elif obj.scene == 5: 
                obj.selectedButton =-1
                UpdateSelectedButton()

                obj.display_text.place(x=80, y=30, anchor="nw")
                obj.display_text.configure(text="* Perdonar\n* Huir\n* Regresar")
                obj.heart_menu.place(x=0.2*obj.screenSize[0], y=0.565*obj.screenSize[1], width=29, height=29)

                selectedMenuButton = 0
                obj.pressed_space = False
                while obj.scene == 5:
                    if Keybind("up"): selectedMenuButton = max(selectedMenuButton-1, 0)
                    if Keybind("down"): selectedMenuButton = min(selectedMenuButton+1, 2)
                    
                    if selectedMenuButton == 0:
                        obj.heart_menu.place_configure(y=0.565*obj.screenSize[1])
                    if selectedMenuButton == 1:
                        obj.heart_menu.place_configure(y=0.622*obj.screenSize[1])
                    if selectedMenuButton == 2:
                        obj.heart_menu.place_configure(y=0.679*obj.screenSize[1])
                    if obj.pressed_space: break

                    while Keybind("up") or Keybind("down"): time.sleep(0.1)
                    time.sleep(0.02)
                obj.pressed_space = False

                obj.display_text.place_forget()
                obj.heart_menu.place_forget()

                if selectedMenuButton == 0:
                    if obj.trust_level >= 99:
                        ## Spare ending
                        obj.Dialogue("* Chikis acepta tu piedad@@@@@\n* Decide no pelear")
                        obj.scene = -3
                    elif obj.spare_condition:
                        ## Spare ending
                        obj.Dialogue("* Chikis acepta tu piedad@@@@@\n* Y se arrastra tristemente")
                        obj.scene = -3
                    elif obj.trust_level < 0:
                        ## Betrayal ending
                        obj.Dialogue("* Chikis acepta tu piedad@@@@@\n* Es broma claro que no")
                        obj.trust_level = -99
                        obj.scene = 1
                    else:
                        obj.Dialogue("* Chikis no acepta tu piedad")
                        obj.scene = 1
                    time.sleep(2)
                elif selectedMenuButton == 1:
                    obj.Dialogue("* Chikis bloquea el camino")
                    time.sleep(2)
                    obj.scene = 1
                else: 
                    obj.scene = 0

                obj.menu_dialogue.place_forget()

            ## When no obj.scene or an invalid one is selected
            else: 
                obj.selectedButton =-1
                UpdateSelectedButton()
    
    threading.Thread(target=_thread, daemon=True).start()

def InputDebug(event):
    obj.trust_level = 999
root.bind("<f>", InputDebug)

def InputSelect(event):
    if obj.scene in [-3, -2, -1, 3, 4, 5]: obj.pressed_space = True
    if obj.scene != 0 or obj.selectedButton == -1: return

    obj.scene = obj.selectedButton+2
root.bind("<space>", InputSelect)
root.bind("<Return>", InputSelect)
root.bind("<z>", InputSelect)

def InputLeft(event):
    if obj.scene != 0 or obj.selectedButton == -1: return

    obj.selectedButton = (obj.selectedButton-1)%4
    UpdateSelectedButton()
root.bind("<Left>", InputLeft)
root.bind("<a>", InputLeft)

def InputRight(event):
    if obj.scene != 0 or obj.selectedButton == -1: return

    obj.selectedButton = (obj.selectedButton+1)%4
    UpdateSelectedButton()
root.bind("<Right>", InputRight)
root.bind("<d>", InputRight)

def UpdateSelectedButton():
    if obj.selectedButton==0: obj.button_fight_image.place_configure(y=-81)
    else: obj.button_fight_image.place_configure(y=0)
    if obj.selectedButton==1: obj.button_act_image.place_configure(y=-81)
    else: obj.button_act_image.place_configure(y=0)
    if obj.selectedButton==2: obj.button_item_image.place_configure(y=-81)
    else: obj.button_item_image.place_configure(y=0)
    if obj.selectedButton==3: obj.button_mercy_image.place_configure(y=-81)
    else: obj.button_mercy_image.place_configure(y=0)

Thread()


def on_close():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
