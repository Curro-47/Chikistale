

from pygame import mixer

mixer.init()

moosic_n_bells = {

#variables sound list
"soundTest" : mixer.Sound("Sounds\\vine-boom.mp3"),
"soundHurt" : mixer.Sound("Sounds\\undertale-damage-taken.mp3"),
"soundHeal" : mixer.Sound("Sounds\\undertale-heal.mp3"),
"soundSelect" : mixer.Sound("Sounds\\undertale-select-sound.mp3"),
"soundSave" : mixer.Sound("Sounds\\undertale-save.mp3"),
"soundSoulShatter" : mixer.Sound("Sounds\\undertale-soul-shatter.mp3"),
"soundAttackLaser" : mixer.Sound("Sounds\\gaster_blaster_sound_effect_1.mp3"),
"soundAttack" : mixer.Sound("Sounds\\undertale-attack-slash-green-screen.mp3"),
"soundBone" : mixer.Sound("Sounds\\bone-undertale-sound-effect.mp3"),
#moosic    
"musicStartMenu" : mixer.Sound("Sounds\\StartMenu.mp3"),
"musicBG1" : mixer.Sound("Sounds\\Bonetrousle.mp3"),
"musicBG2" : mixer.Sound("Sounds\\Dummy.mp3"),
"musicGameOver" : mixer.Sound("Sounds\\Determination.mp3"),
"musicGameOverRevenge" : mixer.Sound("Sounds\\Dogsong.mp3"),
"musicGoodEnding" : mixer.Sound("Sounds\\The Choice.mp3"),
"yourBestNightmare" : mixer.Sound("Sounds\\your-best-nightmare.mp3")

}


#defs
def play_sound(key, vol=1, loops=0):
    moosic_n_bells[key].set_volume(vol)
    moosic_n_bells[key].play(loops=loops)

def pause():
    mixer.pause()

def play():
    mixer.unpause()

def volume_sound(key, vol):
    moosic_n_bells[key].set_volume(vol)

def stop_sound(key):
    moosic_n_bells[key].stop()

def stop_soundAll():
    mixer.stop()