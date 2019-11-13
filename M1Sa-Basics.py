# M1Sa.py - 1. Program
# - Indbygget funktion - print
# - Hjemmelavet funktion og betingelse
# - lister basic
# - random funktion - bibliotek
# - time - bibliotek
# - vise debug step funktion

import random
import time
import pygame

print ("hej med jer")


def pn(t):
    print("Hej med dig: ")
    print(t)
    print("Godt at se dig")
    print("")
          

def lms(n):
    if n<10:
        print("tal under 10")
    elif n == 10:
        print("tal er 10")
    else:
        print("tal over 10")
    

pn("Jens")
pn("Lotte")

lms(5)
lms(24)
lms(10)


jens = "Jens"
print(jens[2])

nl = ["Jens","Peter","Lotte","Marie"]

print(nl[3])

pn(nl[1])

for i in range(4):    # da vi ved listen har 4 indgange. Kunne også bruge len(nl) som mere generisk
    pn(nl[i])


pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load("hej-med-jer.wav")  # works with the file ni same directory as the program else use full path name
pygame.mixer.music.play()


while True:
    pn(random.choice(nl))
    time.sleep(5)
