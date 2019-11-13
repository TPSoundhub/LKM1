# M1Sb.py - Programme with names annoucements
# Revison 1.0 12112019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#
# 
# - Import used libraries

import pygame
import time
import random

# Definition of constants - here text strings to be used later
#
# sti/path for sounds on PC 

sti_navn = "C:/LKM1/lyde/navne-SSG/"
sti_bag  = "C:/LKM1/lyde/baggrund/"
sti_hej  = "C:/LKM1/lyde/hej-ol/"
#
# sti/path for sounds on raspberry PI - A must with full path when program to be started from boot
#
#
#sti_navn = "/home/pi/LKM1/lyde/navne-SSG/"
#sti_bag  = "/home/pi/LKM1/lyde/baggrund/"
#sti_hej  = "/home/pi/LKM1/lyde/hej-ol/"

#
# Names for all in SSG 1.x 2019
#
andreas    = sti_navn+"andreas.wav"
asger      = sti_navn+"asger.wav"
chriss     = sti_navn+"chriss.wav"
helene     = sti_navn+"helene.wav"
kresten    = sti_navn+"kresten.wav"
louise     = sti_navn+"louise.wav"
mads       = sti_navn+"mads.wav"
maten      = sti_navn+"maten.wav"
nicolai    = sti_navn+"nicolai.wav"
patrick    = sti_navn+"patrick.wav"
simon      = sti_navn+"simon.wav"
simon_k    = sti_navn+"simon-k.wav"
tobias     = sti_navn+"tobias.wav"
zuzanna    = sti_navn+"zuzanna.wav"

name_list  = [andreas,asger,chriss,helene,kresten,louise,mads,maten,nicolai,patrick,simon,simon_k,tobias,zuzanna]

#
# Greeting sound 
#
hejmeddig = sti_hej+"hej-med-dig.wav"

#
# Background sounds. Only one is used below Challenge 1 : try the others. Challenge 2: Find other sounds and make them work 
#
regn   = sti_bag+"regn-86sek.wav"
maager = sti_bag+"maager-1min.wav"
trafik = sti_bag+"Trafik-43sek.wav"
f1     = sti_bag+"F1-17sek.wav"
#
# Flag to turn on/off test printouts during test/debugging of programme
#
test_prt = True

#
# Function that can pay 2 sounds in a row.
# - First sound is the greeting sound hejmeddig. Function is named hmd - short for "hej med dig". Challenge : Try out other greetings
# - The second sound is passed to the function as a variable named "n" for name in this context. Used with names from class in this context.
#
# Two more parameters to be given as variables when fuction is called:
# - vl for the volume level in left channel. Must be a value between 0.0 and 1.0, 0.00000 will result in no sound and 1.0 is max
# - vr for the volume level in right channel. Must be a value between 0.0 and 1.0, 0.00000 will result in no sound and 1.0 is max
#
# Different volume in the 2 channels leads to a panning effect. Try it out and experience the effect!
# Note in this function the vl/vr is switched between the 2 sounds played for another effect
#
def hmd(n,vl,vr):
    channel = pygame.mixer.find_channel()
    channel.set_volume(vl,vr)
    channel.play(pygame.mixer.Sound(hejmeddig))
    time.sleep(1)                              # could be smarter using length of sound played instead of fixed value - Challenge: make it smarter!
    channel = pygame.mixer.find_channel()      # Look into pygame mixer documentation to figure out how
    channel.set_volume(vr,vl)                  # switched compared to hejmeddig sound on purpose for giving an effect. Explain effect!
    channel.play(pygame.mixer.Sound(n))
    time.sleep(1)                              # Again could be smarter, and why waiting? Could get the next one no top and have an effect out of that
                                               # Challenge: Experiment with it so next gretting starts on top and does not wait
    

#
# Function to start a backgound sound playing in the SW sound mixer (typically a longer sound file)
#
def sbl(b,v):
    pygame.mixer.music.set_volume(v)
    pygame.mixer.music.load(b)
    pygame.mixer.music.play()

#
# initialization of the SW sound mixer
#
pygame.mixer.init(channels=2)

#
# Greeting to all in alphabetical order and once only and with fixed volume
#
class_size = len(name_list)
for i in range(class_size):
    if test_prt:
        print(name_list[i])
    hmd(name_list[i],0.5,0.5)

#
# For the fun of it and for trying out a program from boot in headless configuraton an infinite loop
# that generates greetings for ever with names in randomised order.
# Volumen in the two channels are also randomised for trying out the effect of it.
# And on top we start a background sound - that only plays once and at a low volume so the names can be heard
#
sbl(trafik,0.1)
while True:
    vol_left = random.uniform(0.0,1.0)
    vol_right = random.uniform(0.0,1.0)
    if test_prt:
        print("vol_right: ", vol_right," vol_left: ",vol_left)
    hmd(random.choice(name_list),vol_right,vol_left)    



