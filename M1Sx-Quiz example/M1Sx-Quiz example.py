# M1Sx-Quizexample.py - Sample code wih a quiz with 12 sounds thats to be matched with keys presses on 4 MB's
# Revison 0.3 28012020, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#
# To be used on WS with teachers 19-feb-2020


#
# Import used Libraries
#
import serial
import pygame
import time
import random


# Definition of constants - here text strings to be used later
#

#
# 12 sounds used for quiz - here bird songs
# All placed in same directory for avoiding to deal with path issues
#
quiz_sound_files = [
"1-stork.wav",      # pos 0  - group 1 sound 1
"2-ugle.wav",       # pos 1  - group 1 sound 2
"3-spaette.wav",    # pos 2  - group 1 sound 3
"4-svale.wav",      # pos 3  - group 2 sound 1
"5-maager.wav",     # pos 4  - group 2 sound 2
"6-pingvin.wav",    # pos 5  - group 2 sound 3
"7-skovskade.wav",  # pos 6  - group 3 sound 1
"8-goeg.wav",       # pos 7  - group 3 sound 2
"9-solsort.wav",    # pos 8  - group 3 sound 3
"10-hane.wav",      # pos 9  - group 4 sound 1
"11-gaes.wav",      # pos 10 - group 4 sound 2
"12-laerk.wav"      # pos 11 - group 4 sound 3
]

baggrundslyd = [
"bagg-trafik.wav",
"bagg-by.wav",
"bagg-cafe.wav",
"bagg-flod.wav"
]

cheer_or_buh_sounds = [
"cheer-crowd.wav",
"buu-trombone.wav"
]


#
# Names on MBs that you want to listen to
#
mb_grp_names = [
#0123456789
"LKM1-1    ",  # group 1
"LKM1-2    ",  # group 2
"LKM1-3    ",  # group 3
"LKM1-4    ",  # group 4
"          ",  # group 5
"          ",  # group 6
"          "   # group 7
]

#
#
# Events we want to react on in this program defined in table below
#
# A,B (from local conneced MB) for switching between quiz and learning mode
# H,V (from local connected MB) for turning up/dn background for making listening easier/harder wrt quiz sounds
# c,p,i from 3 remotes and C,P,I from local connected used as the 12 inputs connected to the 12 bird songs
#
#
key_events              = ["A","B","H","V","C","P","I","a","b","h","v","c","p","i"]
last_key_pressed        = None   # Set the initial value of last pressed key to None as we have not yet received any from the MB yet 

#
# Flags for controlling:
# - test_on: printouts on/off for test/debug/understanding what is happening
# - run_in-gui: To make things different if needed when program is to be run from boot/cli (command line)
#
test_on = True
test_print_1 = False
run_in_gui = True


ser = serial.Serial(timeout=2)
ser.baudrate = 115200
ser.port = "COM14"    # on PC/Windows  number can change to 2.3.4....
# ser.port = "/dev/ttyACM0" # On PI/Raspbian  0 might change to 1.2.3..
# ser.port = "/dev/tty.usbmodem14102" # On MAC the number changing is the 14x00
#

def receive_char():
    microbitdata = str(ser.readline())
    if test_print_1: print(len(microbitdata),microbitdata)
    if len(microbitdata)>3:
        if run_in_gui :
            key = microbitdata[2]
            sender = microbitdata[4:14]
        else:
            key = microbitdata[0]
            sender = microbitdata[2:12]
        if (key not in key_events): key="0" # meaning not a relevant key
        # in this context we do not differentiate local vs remote for cpiCPI so convert CPI to cpi here to make easier in main loop
        # we use group to identify
        if key == "C": key = "c"
        if key == "P": key = "p"
        if key == "I": key = "i"

        gr = "0" # meaning sender not in group of relevant senders
        if   sender == mb_grp_names[0]: gr = "1"  # could be done smarter by fixed table lookup dict..
        elif sender == mb_grp_names[1]: gr = "2"
        elif sender == mb_grp_names[2]: gr = "3"
        elif sender == mb_grp_names[3]: gr = "4"
        elif sender == mb_grp_names[4]: gr = "5"
        elif sender == mb_grp_names[5]: gr = "6"
        elif sender == mb_grp_names[6]: gr = "7"
        return key, gr # when there is no relevant key or group -> no relevant key input for this programme return values are "0" and "0"
    else: return None, None  # when there is a timeout on the inputs -> no key pressed


#
# returning channel gives the option to change dymamically in volumen for the channel - eg make pan effect
# t for times to play sound in the channel. -1 means repeat until stopped
#
def play_sound(n,t,vl,vr):
    channel = pygame.mixer.find_channel()
    channel.set_volume(vl,vr)
    channel.play(pygame.mixer.Sound(n),t)
    return channel

              
#
# Pygame initialising wrt sound mixer and selected sound samples
#

pygame.mixer.init(channels=2)

# variable for the volume level for background sound playback
# used as a global varialble that is changed during program execution on input events later
# set for a starting volume of 0.1
#
music_volume=0.0
#
# set the sound volumen for sound to be played on top to a fixed value.
# Challenge - play around with them eg as a result of some input event from the Microbit
# can the panning within the 2 stereo channels be used for something?
#
ch_vol_right = 0.5
ch_vol_left  = 0.5

mode = "practice"
bagg_idx = 0
playing_idx = 0


#
# Start playback of the background sound selected
#
def play_background(bg):
    pygame.mixer.music.load(bg)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)                       # minus one as function input gives an infinite playback loop of the sound!


#
# Functios made for the reason of making main loop more readable
# Hence the "global" for referencing/scoping the variable correct 
#

def play_key_sound(rc,group_offset):
    global last_key_pressed, ch, ch_vol_right, ch_vol_left
    if rc == "c" and last_key_pressed != "c":
        ch = play_sound(quiz_sound_files[group_offset],0,0.5,0.5)
        ch_vol_right = 0.5
        ch_vol_left  = 0.5
    if rc == "p" and last_key_pressed != "p":
        ch = play_sound(quiz_sound_files[group_offset+1],0,0.5,0.5)
        ch_vol_right = 0.5
        ch_vol_left  = 0.5
    if rc == "i" and last_key_pressed != "i":
        ch = play_sound(quiz_sound_files[group_offset+2],0,0.5,0.5)
        ch_vol_right = 0.5
        ch_vol_left  = 0.5    
    last_key_pressed = rc


def background_volume(rc):
    global music_volume
    if rc == "V":
        if music_volume<1.0: music_volume=music_volume+0.05
        if test_on:print("Vol up: ", music_volume)
    elif rc == "H":
        if music_volume>0.0: music_volume=music_volume-0.05
        if test_on: print("Vol down: ", music_volume)
    pygame.mixer.music.set_volume(music_volume)


def pan_last_channel(rc):
    global ch_vol_right, ch_vol_left
    if rc == "v":
        if ch_vol_right<1.0:
            ch_vol_right=ch_vol_right+0.1
            if ch_vol_right>1.0: ch_vol_right = 1.0
        if ch_vol_left>0.0:
            ch_vol_left=ch_vol_left-0.1
            if ch_vol_left<0: ch_vol_left=0
        if test_on:print("pan right (l,r): ", ch_vol_left,ch_vol_right)
    elif rc == "h":
        if ch_vol_right>0.0:
            ch_vol_right=ch_vol_right-0.1
            if ch_vol_right<0: ch_vol_right = 0
        if ch_vol_left<1.0:
            ch_vol_left=ch_vol_left+0.1
            if ch_vol_left>1.0: ch_vol_left = 1.0
        if test_on:print("pan left (l,r): ", ch_vol_left,ch_vol_right)
    ch.set_volume(ch_vol_left,ch_vol_right)

def change_background(rc):
    global bagg_idx
    if bagg_idx==0: bagg_idx=3
    else: bagg_idx=bagg_idx-1
    play_background(baggrundslyd[bagg_idx])

def check_correct_answer(rc,group_offset):
    global playing_idx, ch
    i=100 # for index out of range
    if   rc == "c": i=group_offset
    elif rc == "p": i=group_offset+1
    elif rc == "i": i=group_offset+2
    if i == playing_idx:
        ch.stop() # stop playing sound
        ch_tmp = play_sound(cheer_or_buh_sounds[0],0,0.5,0.5) # cheer for correct answer
        time.sleep(10)
        playing_idx = random.randint(0,len(quiz_sound_files)-1)
        if test_on: print("entering quiz mode with idx sound playing: ",playing_idx)
        ch = play_sound(quiz_sound_files[playing_idx],-1,0.5,0.5)  # start new random sound

    elif i < 100:
        ch_tmp = play_sound(cheer_or_buh_sounds[1],0,0.5,0.5) # buuh for wrong answer


#
# initialise seriel port and background playing
# also play one sound in channel to get ch defined in case any pan cammond gets invoked
#
ser.open()
play_background(baggrundslyd[bagg_idx])
ch = play_sound("start-seq.wav",0,0.3,0.3)


# Loop forever

while True:

    rc,gr = receive_char()
    if (gr == None and rc == None):
        if test_print_1: print("timeout")
        last_key_pressed = None

    if gr != None:
        if test_on: print(rc, gr)
        if rc == "H" or rc == "V": background_volume(rc)
        if rc == "h" or rc == "v": pan_last_channel(rc)
        if rc == "a" or rc == "b": change_background(rc)
        
        if rc == "A":
            mode = "practice"
            ch.stop() # stop playing sound
        if rc == "B":
            mode = "quiz"      
            ch.stop() # stop playing sound if already one active when pressing "B" (second press without any guess
            playing_idx = random.randint(0,len(quiz_sound_files)-1)
            if test_on:
                print("entering quiz mode with idx sound playing: ",playing_idx)
                print(len(quiz_sound_files))
            ch = play_sound(quiz_sound_files[playing_idx],-1,0.5,0.5)

        
        if mode == "practice":
            if   gr == "1": play_key_sound(rc,0)
            elif gr == "2": play_key_sound(rc,3)
            elif gr == "3": play_key_sound(rc,6)
            elif gr == "4": play_key_sound(rc,9)
        if mode == "quiz":
            if test_on: print("quiz mode")
            if   gr == "1": check_correct_answer(rc,0)
            elif gr == "2": check_correct_answer(rc,3)
            elif gr == "3": check_correct_answer(rc,6)
            elif gr == "4": check_correct_answer(rc,9)
        
 


