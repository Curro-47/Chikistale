

from pygame import mixer

mixer.init()

moosic_n_bells = {

#variables sound list
"soundTest" : mixer.Sound("mp3tale\\vine-boom.mp3"),
"soundHurt" : mixer.Sound("mp3tale\\undertale-damage-taken.mp3"),
"soundHeal" : mixer.Sound("mp3tale\\undertale-heal.mp3"),
"soundSelect" : mixer.Sound("mp3tale\\undertale-select-sound.mp3"),
"soundSave" : mixer.Sound("mp3tale\\undertale-save.mp3"),
"soundSoulShatter" : mixer.Sound("mp3tale\\undertale-soul-shatter.mp3"),
"soundAttackLaser" : mixer.Sound("mp3tale\\gaster_blaster_sound_effect_1.mp3"),
#moosic    
"musicBG1" : mixer.Sound("mp3tale\\Bonetrousle.mp3"),
"musicBG2" : mixer.Sound("mp3tale\\Dummy.mp3"),
"musicGameOver" : mixer.Sound("mp3tale\\Determination.mp3"),
"musicGameOverRevenge" : mixer.Sound("mp3tale\\Dogsong.mp3"),
"musicGoodEnding" : mixer.Sound("mp3tale\\The Choice.mp3"),
"yourBestNightmare" : mixer.Sound("mp3tale\\your-best-nightmare.mp3")

}


#defs
def play_sound(key):
    moosic_n_bells[key].play()

def stop_sound(key):
    moosic_n_bells[key].stop()

def stop_soundAll():
    mixer.stop()