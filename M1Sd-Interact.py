# M1Sd-Interact.py - Sample code wih MB input to interact with sound
# Revison 1.0 12112019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#
# This code can be the basic for your own project building a program that interacts with the Microbit with the given code
# and playing back some sound based on the input and purhaps other stuff in this program.
#
# Challenge: Not to wait forever on inputs from Microbit, but also do7check for other events within this program
# Hint - see M1Sc-FindMBserial for a hint regarding timeout on reading from the serial port
#
# Challenge: Make a better structure than the if elif's for handling state/events and actions
# BUT be aware of the time limits and contraints. You must have a result to present in short time
# SO where and in which processes are the time best spent????
#
# The code in the Microbit gives you 2 sets of inputs - On from a local connected MB and from a remote one.
# It is differentialted by receiving BIG vs small letters for input event. Vhallenge: How to use that in your project?
#
# There also is a way to differentiate between more than one remote. HOW? and can that be used?
#
#
#
# Import used Libraries
#
import serial
import pygame


# Definition of constants - here text strings to be used later
#
# sti/path for sounds on PC 

sti_bag  = "C:/LKM1/lyde/baggrund/"
sti_div  = "C:/LKM1/lyde/div/"
#
# sti/path for sounds on raspberry PI - A must with full path when program to be started from boot
# For the MAC it is similar - ....
#
#sti_bag  = "/home/pi/LKM1/lyde/baggrund/"
#sti_hej  = "/home/pi/LKM1/lyde/hej-ol/"


#
# 3 sound used in thes program example
# Challenge 1 : Try some other sounds in the given directories
# Challenge 2 : Try more sounds on more input events
# Challenge 3 : Find other sounds and use them instead.
# - Eiter find on internet eg freesound.org
# - or record some yourself. Use eg Audacity for sound editing and resampling (if needed)
# Be aware they should be keept short and in wav stereo format
#

baggrundslyd = sti_bag+"Trafik-43sek.wav"
lyd1 = sti_div+"Ding-1sek.wav"
lyd2 = sti_div+"Crash-2sek.wav"


# include full path to sounds on PI
# baggrundslyd = "/home/pi/LKM1/lyde/"
# lyd1 = "/home/pi/LKM1/Lyd1.wav"
# lyd2 = "/home/pi/LKM1/Lyd2.wav"


#
# Flags for controlling:
# - test_on: printouts on/off for test/debug/understanding what is happening
# - run_in-gui: To make things different if needed when program is to be run from boot/cli (command line)
#

test_on = True
run_in_gui = True

#
# Set up the Serial connection to capture the Microbit communications
# Find the right port as USB devices are identified and remembered in case they come back
# ON Windows/PC the name/number used are "COM#", where # is the number - Use M1Sc-VisSeriel to find the right port
# ON Raspbian/PI the name/number is "/dev/ttvACM#", where # is the number - Use M1Sc-VisSeriel to find the right port
# ON MAC the name/number is "/dev/tty.usbmodem14#02", where # is the number - Use M1Sc-Visseriel to find the right port
# Challenge - integrate code from M1Sc-FindMBserial into final projekct code to make MB detection more roboust.
#

ser = serial.Serial()                                                         
ser.baudrate = 115200
ser.port = "COM4"    # on PC/Windows  number can change to 2.3.4....
# ser.port = "/dev/ttyACM0" # On PI/Raspbian  0 might change to 1.2.3..
# ser.port = "/dev/tty.usbmodem14102" # On MAC the number changing is the 14x00
#

ser.open()

def receive_char():
    # Read in a line from the Microbit, store it in variable 'microbitdata' as a string and then clean it up to only the character sent from microbit
    microbitdata = str(ser.readline())
    if test_on: print("received input: ",microbitdata)
    if run_in_gui:
        char_received = microbitdata[2]
    else:
        char_received = microbitdata[0]
    if test_on: print("treated input: ",char_received)
    return char_received



def play_sound(n,vl,vr):
    channel = pygame.mixer.find_channel()
    channel.set_volume(vl,vr)
    channel.play(pygame.mixer.Sound(n))
              
#
# Pygame initialising wrt sound mixer and selected sound samples
#

pygame.mixer.init(channels=2)



# variable for the volume level for background sound playback
# used as a global varialble that is changed during program execution on input events later
# set for a starting volume of 0.1
#
music_volume=0.1                                  

#
# Start playback of the background sound selected
#
pygame.mixer.music.load(baggrundslyd)
pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.play(-1)                       # minus one as function input gives an infinite playback loop of the sound!

#
# set the sound volumen for sound to be played on top to a fixed value.
# Challenge - play around with them eg as a result of some input event from the Microbit
# can the panning within the 2 stereo channels be used for something?
#
sound_vol_right = 0.5
sound_vol_left  = 0.5



# Loop forever

while True:

    rc = receive_char()
    
    if rc == "H" or rc == "h":
        if music_volume<1.0:
            music_volume=music_volume+0.02
            pygame.mixer.music.set_volume(music_volume)
            if test_on:
                print("Vol up")
                print(music_volume)
    elif rc == "V" or rc == "v":
        if music_volume>0.0:
            music_volume=music_volume-0.02
            pygame.mixer.music.set_volume(music_volume)
            if test_on:
                print("Vol down")
                print(music_volume)
    elif rc == "S" or rc == "s":
        if test_on: print("Hvad skal vi lave med en S/s ved skift til high lys intensitet?")
    elif rc == "D" or rc == "d":
        if test_on: print("Hvad skal vi lave med en D/d ved skift til normal lys intensitet?")
    elif rc == "N" or rc == "n":
        if test_on: print("Hvad skal vi lave med en N/n ved skift til lav lys intensitet?")
    elif rc == "F" or rc == "f":
        if test_on: print("Hvad skal vi lave med en F/f ved tilt frem?")
    elif rc == "T" or rc == "t":
        if test_on: print("Hvad skal vi lave med en T/t ved tilt tilbage?")
    elif rc == "C" or rc == "c":
        if test_on: print("Hvad skal vi lave på en C/c ved pin 1 aktiveret?")
    elif rc == "0" or rc == "1" or rc == "2" or rc == "3" or rc == "4" or rc == "5" or rc == "6" or rc == "7" or rc == "8" or rc == "9":
        if test_on: print("Hvad skal vi lave på 0-9 ved pin 2 aktiveret?")
    elif rc == "A" or rc == "a":
        if test_on: print("Sound 1 on top")
        play_sound(lyd1,sound_vol_right,sound_vol_left)
    elif rc == "B" or rc == "b":
        if test_on: print("Sound 2 on top")
        play_sound(lyd2,sound_vol_right,sound_vol_left)
    




