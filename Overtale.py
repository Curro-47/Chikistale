from tkinter import *
from tkinter import font as tkFont
import math
import time
import keyboard
import threading

## Local file imports
import Scripts.TkinterShapes as ts
import Scripts.Attacks as attacks
import Scripts.CustomFonts as cFonts

## Setup tkinter window
root = Tk()
root.configure(bg='black')
root.geometry("1280x720")
root.resizable(False, False) 

## Prepare variables
scene = 0 # 0 menu, 1 battle, 2 attack, 3 act, 4 item, 5 mercy
selectedButton = 0

## Customization
menuSize = (0.7, 0.3)
screenSize = (1280, 720)
lineWidth = screenSize[0]/100

max_health = 20
health = max_health
max_damage = 50

used_chikiramen = False
pressed_space = False
spare_condition = False

boss_max_health = 100
boss_health = boss_max_health

## Import sprites and fonts
img_boss = PhotoImage(file="Sprites\\placeholder.png").subsample(5, 5)
img_heart = PhotoImage(file="Sprites\\heart.png").subsample(32, 32)
img_buttons = PhotoImage(file="Sprites\\battle_buttons.png")
img_hp = PhotoImage(file="Sprites\\hp.png")
img_target = PhotoImage(file="Sprites\\target.png").zoom(3,3).subsample(2,2)
img_target_aim = PhotoImage(file="Sprites\\target_aim.png").zoom(3,3).subsample(2,2)
img_target_aim2 = PhotoImage(file="Sprites\\target_aim2.png").zoom(3,3).subsample(2,2)
img_text = PhotoImage(file="Sprites\\text.png")

cFonts.loadfont(b"Fonts\\DeterminationMonoWebRegular-Z5oq.ttf")
font_determination = tkFont.Font(family="Determination Mono Web", size=12)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Determination Mono Web", size=12)

ts.Init(screenSize, lineWidth)

## Create objects
boss, _ = ts.ImageSquare(root, x=0.5, y=0.3, w=0.2, rh=1, image=img_boss, offset=(0.5, 0.5))
menu, menu_border = ts.Square(root, x=0.5, y=0.65, w=menuSize[0], h=menuSize[1])
menu_dialogue = Label(menu, text="None", bg='black', fg='white')
heart = menu.create_image(menuSize[0]*screenSize[0]/2, menuSize[1]*screenSize[1]/2, image=img_heart)
heart_menu, _ = ts.ImageSquare(root, image=img_heart, x=0.5, y=0.5, w=29, rh=1, relative=False, image_anchor="nw")
heart_menu.place_forget()

attacks.Init(menu, [0.3*screenSize[1], 0.3*screenSize[1]])
atk = attacks.Attacks()

debug = Label(root, text="Debug")
debug.place(x=0, y=0)

info_name = ts.TextSquare(root, text="CURRO  LV 1", size=30, x=0.25, y=0.875, anchor="sw")
info_hp_text, _ = ts.ImageSquare(root, x=0.45, y=0.865, w=0.05, rh=0.5, image=img_hp, offset=(0.5, 0.5), anchor="sw", image_anchor=CENTER)
info_hp_frame = ts.FillSquare(root, x=0.50, y=0.87, w=0.049, h=0.05, bg='red3', anchor="sw")
info_hp_bar = ts.FillSquare(info_hp_frame, x=-0.001, y=0, w=0.05, h=0.05, bg='yellow', anchor="nw")
info_hp_display = ts.TextSquare(root, text="20/20", size=30, x=0.56, y=0.875, anchor="sw")

button_fight, button_fight_image = ts.ImageSquare(root, image=img_buttons, x=0.2, y=0.88, w=170, h=70, relative=False, anchor="nw", image_anchor="nw", offset=(0,0))
button_act, button_act_image = ts.ImageSquare(root, image=img_buttons, x=0.36, y=0.88, w=170, h=70, relative=False, anchor="nw", image_anchor="nw", offset=(-1.05,0))
button_item, button_item_image = ts.ImageSquare(root, image=img_buttons, x=0.64, y=0.88, w=170, h=70, relative=False, anchor="ne", image_anchor="nw", offset=(-2.1,0))
button_mercy, button_mercy_image = ts.ImageSquare(root, image=img_buttons, x=0.8, y=0.88, w=170, h=70, relative=False, anchor="ne", image_anchor="nw", offset=(-3.15,0))

attack_menu = Canvas(menu, bg='black')
attack_target = attack_menu.create_image(screenSize[0]*menuSize[0]/2-screenSize[0]/100, screenSize[1]*menuSize[1]/2+screenSize[0]/200, image=img_target)
attack_aim = attack_menu.create_image(0, screenSize[1]*menuSize[1]/2+screenSize[0]/200, image=img_target_aim)

boss_health_base = ts.FillSquare(root, x=0.5, y=0.15, w=0.15, h=0.04, bg='gray26')
boss_health_bar = ts.FillSquare(boss_health_base, x=0, y=0, w=0.15, h=0.04, bg='green3', anchor="nw")
boss_damage_number0, bdn0 = ts.ImageSquare(root, x=0.48, y=0.09, w=0.0457, rh=1, image=img_text, image_anchor="nw", offset=cFonts.char(8))
boss_damage_number1, bdn1 = ts.ImageSquare(root, x=0.52, y=0.09, w=0.0457, rh=1, image=img_text, image_anchor="nw", offset=cFonts.char(7))

boss_health_base.place_forget()
boss_damage_number0.place_forget()
boss_damage_number1.place_forget()

display_text = Label(menu, text="* Chiki-ramen", bg='black', fg='white', justify="left")

def Dialogue(txt):
    global menuSize
    thread = ts.Resize(menu_border, subObject=menu, w=0.67, h=0.3)
    menuSize = (0.67, 0.3)
    thread.join()

    menu_dialogue.configure(text = "")
    menu_dialogue.place(x=20, y=20)
    txtNew = ""

    for chr in txt:
        txtNew = txtNew + chr
        menu_dialogue.configure(text=txtNew)
        time.sleep(0.05)


def Kill():
    pass

def Damage(dmg):
    global health, max_health
    health -= dmg

    if health > max_health: 
        health = max_health
    elif health <= 0:
        health = 0
        Kill()
    
    healthDisplay = str(health).zfill(2)+"/"+str(max_health).zfill(2)
    info_hp_display.configure(text=healthDisplay)

    info_hp_bar.place_configure(width=0.05*screenSize[0]*(health/max_health))

def DamageBoss(dmg):
    def _thread():
        global boss_health, boss_max_health, menuSize
        startBossHealth = boss_health

        boss_health_base.place(x=0.5*screenSize[0], y=0.15*screenSize[1], width=0.15*screenSize[0], height=0.04*screenSize[1], anchor=CENTER)

        ## Place damage numbers
        boss_damage_number0.place(x=0.48*screenSize[0], y=0.09*screenSize[1], width=0.0457*screenSize[0], height=0.0457*screenSize[0], anchor=CENTER)
        if dmg>=10: boss_damage_number1.place(x=0.52*screenSize[0], y=0.09*screenSize[1], width=0.0457*screenSize[0], height=0.0457*screenSize[0], anchor=CENTER)
        
        bdn0.place_configure(x=cFonts.char(int(str(dmg)[0]))[0]*0.0457*screenSize[0])
        if dmg>=10: bdn1.place_configure(x=cFonts.char(int(str(dmg)[1]))[0]*0.0457*screenSize[0])
        
        if dmg<10: boss_damage_number0.place_configure(x=0.5*screenSize[0])

        loopStartGlobalTime = time.time()
        while True:
            loopTime = time.time() - loopStartGlobalTime
            if loopTime > 1: break

            boss_health = startBossHealth - (dmg*loopTime)

            boss_health_bar.update()
            boss_health_bar.place_configure(width=(0.15*screenSize[0]*(boss_health/boss_max_health)))

            ## Shake animation
            shake = math.sin(loopTime*40)*20 * (1-loopTime)
            shake = math.tanh(8 * math.sin(loopTime*40))*20 * (1-loopTime)

            boss.place_configure(x=0.5*screenSize[0]+shake, anchor=CENTER)

            ## Number animation
            jump = math.sin(loopTime/0.75 * math.pi)*25
            if loopTime > 0.75: jump = 0

            boss_damage_number0.place_configure(y=0.09*screenSize[1] - jump)
            boss_damage_number1.place_configure(y=0.09*screenSize[1] - jump)

            time.sleep(0.02)

        time.sleep(0.5)
        boss_health_base.place_forget()
        boss_damage_number0.place_forget()
        boss_damage_number1.place_forget()
    threading.Thread(target=_thread, daemon=True).start()

def Thread():
    def _thread():
        while True:
            global selectedButton, scene, used_chikiramen, pressed_space
            #### NOT FIGHTMODE (Menu)
            if scene == 0:
                thread = ts.Resize(menu_border, subObject=menu, w=0.67, h=0.3)
                menuSize = (0.67, 0.3)

                selectedButton =-1
                heartPos = menu.coords(heart)
                menu.move(heart, -heartPos[0]-40, -heartPos[1]-40)

                thread.join()
                selectedButton =0
                UpdateSelectedButton()

                while scene == 0: pass
            
            #### FIGHTMODE
            elif scene == 1:
                thread = ts.Resize(menu_border, subObject=menu, w=0.3/screenSize[0]*screenSize[1], h=0.3)
                selectedButton =-1
                UpdateSelectedButton()
                menuSize = (0.3/screenSize[0]*screenSize[1], 0.3)
                thread.join()

                battleStartGlobalTime = time.time()

                heartPos = menu.coords(heart)
                menu.move(heart, -heartPos[0]+screenSize[0]*menuSize[0]/2 -3, -heartPos[1]+screenSize[1]*menuSize[1]/2 -3)
                
                atk.atk_sparkgrid(0)

                while scene == 1:
                    battleTime = time.time() - battleStartGlobalTime

                    heartPos = menu.coords(heart)
                    ## Movement
                    speed = 0.65
                    if keyboard.is_pressed("left"): menu.move(heart, -speed, 0)
                    if keyboard.is_pressed("right"): menu.move(heart, speed, 0)
                    if keyboard.is_pressed("up"): menu.move(heart, 0, -speed)
                    if keyboard.is_pressed("down"): menu.move(heart, 0, speed)

                    ## offsetLeft, offsetUp, offsetRight, offsetDown
                    offset = [heartPos[0]-15, heartPos[1]-15, (menuSize[0]*screenSize[0])-heartPos[0]-30, (menuSize[1]*screenSize[1])-heartPos[1]-30]
                    
                    ## Collision with borders
                    if offset[0] < 0: menu.move(heart, -offset[0], 0)
                    if offset[1] < 0: menu.move(heart, 0, -offset[1])
                    if offset[2] < 0: menu.move(heart, offset[2], 0)
                    if offset[3] < 0: menu.move(heart, 0, offset[3])

                    time.sleep(0.002)
            
            ## Attack scene
            elif scene == 2:
                thread = ts.Resize(menu_border, subObject=menu, w=0.67, h=0.3)
                menuSize = (0.67, 0.3)
                thread.join()

                attack_menu.place(x=-screenSize[0]/100, y=-screenSize[0]/100, width = screenSize[0]*menuSize[0]+screenSize[0]/100, height = screenSize[1]*menuSize[1]+screenSize[0]/100, anchor="nw")
                attack_aim = attack_menu.create_image(0, screenSize[1]*menuSize[1]/2+screenSize[0]/200, image=img_target_aim)

                selectedButton =-1
                UpdateSelectedButton()


                attackStartGlobalTime = time.time()
                while scene == 2:
                    attackTime = time.time() - attackStartGlobalTime
                    if attackTime < 0.5: continue

                    attack_menu.move(attack_aim, 12, 0)
                    if keyboard.is_pressed("space"): break
                    if attackTime > 2.2: break

                    time.sleep(0.02)

                attackStartGlobalTime = time.time()
                
                def AnimAim():
                    attackTime = time.time() - attackStartGlobalTime
                    while attackTime < 0.75:
                        attackTime = time.time() - attackStartGlobalTime

                        attack_menu.itemconfigure(attack_aim, image=img_target_aim2)
                        time.sleep(0.08)
                        attack_menu.itemconfigure(attack_aim, image=img_target_aim)
                        time.sleep(0.08)
                    attack_menu.delete(attack_aim)
                    attack_menu.place_forget()
                anim_aim = threading.Thread(target=AnimAim, daemon=True)
                anim_aim.start()

                time.sleep(0.5)

                # Calculate damage
                dmg = round((435.75 - abs(436 - attack_menu.coords(attack_aim)[0]))/436 * max_damage)
                if dmg < 0: dmg = 0
                DamageBoss(dmg)

                anim_aim.join()

                scene = 1

            ## Act scene
            elif scene == 3:
                selectedButton =-1
                UpdateSelectedButton()

                display_text.place(x=80, y=30, anchor="nw")
                display_text.configure(text="* Inspeccionar     * Coquetear\n* Platicar         * Regresar")
                heart_menu.place(x=0.2*screenSize[0], y=0.565*screenSize[1], width=29, height=29)

                selectedMenuButton = [0, 0]
                while scene == 3:
                    if keyboard.is_pressed("Left"): selectedMenuButton[0] = 0
                    if keyboard.is_pressed("Right"): selectedMenuButton[0] = 1
                    if keyboard.is_pressed("Up"): selectedMenuButton[1] = 0
                    if keyboard.is_pressed("Down"): selectedMenuButton[1] = 1
                    
                    if selectedMenuButton == [0,0]: heart_menu.place_configure(x=0.2*screenSize[0], y=0.565*screenSize[1])
                    if selectedMenuButton == [0,1]: heart_menu.place_configure(x=0.2*screenSize[0], y=0.622*screenSize[1])
                    if selectedMenuButton == [1,0]: heart_menu.place_configure(x=0.5*screenSize[0], y=0.565*screenSize[1])
                    if selectedMenuButton == [1,1]: heart_menu.place_configure(x=0.5*screenSize[0], y=0.622*screenSize[1])

                    if pressed_space: break
                pressed_space = False

                display_text.place_forget()
                heart_menu.place_forget()

                if selectedMenuButton == [0, 0]:
                    scene = 1
                elif selectedMenuButton == [0, 1]:
                    scene = 1
                elif selectedMenuButton == [1, 0]:
                    scene = 1
                elif selectedMenuButton == [1, 1]:
                    scene = 0

            ## Items scene
            elif scene == 4:
                selectedButton =-1
                UpdateSelectedButton()

                display_text.place(x=80, y=30, anchor="nw")
                heart_menu.place(x=0.2*screenSize[0], y=0.565*screenSize[1], width=29, height=29)

                if (used_chikiramen):
                    display_text.configure(text="* Regresar\n\nNo tienes objetos")

                    while keyboard.is_pressed("space"): time.sleep(0.02)
                    while not keyboard.is_pressed("space"): time.sleep(0.02)

                    display_text.place_forget()
                    heart_menu.place_forget()

                    scene = 0
                else:
                    display_text.configure(text="* Chiki-ramen\n* Regresar")

                    selectedMenuButton = 0
                    while scene == 4:
                        if keyboard.is_pressed("Up"): selectedMenuButton = 0
                        if keyboard.is_pressed("Down"): selectedMenuButton = 1
                        
                        if selectedMenuButton == 0:
                            heart_menu.place_configure(y=0.565*screenSize[1])
                        if selectedMenuButton == 1:
                            heart_menu.place_configure(y=0.622*screenSize[1])
                        if pressed_space: break
                    pressed_space = False

                    display_text.place_forget()
                    heart_menu.place_forget()

                    if selectedMenuButton == 0:
                        Damage(-20)

                        Dialogue("* Comiste el Chiki-Ramen")
                        time.sleep(2)

                        menu_dialogue.place_forget()
                        used_chikiramen = True

                        scene = 1
                    else:
                        scene = 0
                pressed_space = False

            ## Mercy scene
            elif scene == 5: 
                selectedButton =-1
                UpdateSelectedButton()

                display_text.place(x=80, y=30, anchor="nw")
                display_text.configure(text="* Perdonar\n* Huir")
                heart_menu.place(x=0.2*screenSize[0], y=0.565*screenSize[1], width=29, height=29)

                selectedMenuButton = 0
                while scene == 5:
                    if keyboard.is_pressed("Up"): selectedMenuButton = 0
                    if keyboard.is_pressed("Down"): selectedMenuButton = 1
                    
                    if selectedMenuButton == 0:
                        heart_menu.place_configure(y=0.565*screenSize[1])
                    if selectedMenuButton == 1:
                        heart_menu.place_configure(y=0.622*screenSize[1])
                    if pressed_space: break
                pressed_space = False

                display_text.place_forget()
                heart_menu.place_forget()

                if selectedMenuButton == 0:
                    if boss_health < 10:
                        scene = -1
                    elif spare_condition:
                        scene = -2
                    else:
                        Dialogue("* BLOQUE DE RUTENIO no acepta tu piedad")
                        scene = 1
                else:
                    Dialogue("* BLOQUE DE RUTENIO bloquea el camino")
                    scene = 1
                time.sleep(2)
                menu_dialogue.place_forget()

            ## When no scene or an invalid one is selected
            else: 
                selectedButton =-1
                UpdateSelectedButton()
    
    threading.Thread(target=_thread, daemon=True).start()

def InputDebug(event):
    global scene
    if scene == 0: scene = 1
    else: scene = 0

    Damage(1)
root.bind("<f>", InputDebug)

def InputSelect(event):
    global selectedButton, scene, pressed_space
    if scene == 5 or scene == 4 or scene == 3: pressed_space = True
    if scene != 0 or selectedButton == -1: return

    scene = selectedButton+2
root.bind("<space>", InputSelect)

def InputLeft(event):
    global selectedButton
    if scene != 0 or selectedButton == -1: return

    selectedButton = (selectedButton-1)%4
    UpdateSelectedButton()
root.bind("<Left>", InputLeft)

def InputRight(event):
    global selectedButton
    if scene != 0 or selectedButton == -1: return

    selectedButton = (selectedButton+1)%4
    UpdateSelectedButton()
root.bind("<Right>", InputRight)

def UpdateSelectedButton():
    if selectedButton==0: button_fight_image.place_configure(y=-81)
    else:button_fight_image.place_configure(y=0)
    if selectedButton==1: button_act_image.place_configure(y=-81)
    else: button_act_image.place_configure(y=0)
    if selectedButton==2: button_item_image.place_configure(y=-81)
    else: button_item_image.place_configure(y=0)
    if selectedButton==3: button_mercy_image.place_configure(y=-81)
    else: button_mercy_image.place_configure(y=0)

Thread()
root.mainloop()
