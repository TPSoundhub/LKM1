# Basic event maker for LYDKit project P1 winter 2019. SSG, SHD, Herningsholm, Skanderborg - sponsered by Region MidtJylland
# Version 12 september 2019, Knud Funch SHD
# - Added basic filtering on accelerometer input - removing spike readings
#
# Version 9th september 2019, Knud Funch SHD:
#
# Send string "Hello world ..." on serial USB and make Happy face on LEDs when powerup
# Send characters on serial USB
# - "A", "B" when key a/b is pressed - plus "A" "B" on local display - Once pr press
# - "C" when pin 0 is activated - repetivive as long as pin 0 is active whith 500ms spacing
# - "0" - "9" randomly selected when pin 1 is active - repetivite 500ms spacing
# - "V" - when tilted to left   - repetitive 500ms spacing
# - "H" - When tilted to right  - repetitive 500ms spacing
# - "F" - when tilted forward   - repetitive 500ms spacing
# - "T" - when tilted backwards - repetitive 500ms spacing
#
# - Switch mode between sending on radio ws sending on serial when pin 2 is active
#    - small square followed by big square -> Radio tansmission
#    - big square follwed by small square -> Serial transmission
# If transmisson on radio then feedback on LED are in small letters "a","b" etc..
#     - and so is the character transmitted.
#     - Digits not transmitted so no action on pin 1 when in radio transmission mode.
# If anything is received on radio the received character is sent on serial USB. No feedback on LEDs
#
from microbit import *
import random
import radio


radio.on()                                     # Turn on radio module so it can send and receive messages - do use some extra power!
on_radio = False                               # Global variable to decide whether or not to send character on radio

def clear_disp():
    sleep(500)
    display.clear()

def send_on_radio(s):
    # To identify inputs from radio compared to those from local make small letters from capital letters
    if s == "A": s_low = "a"
    elif s == "B": s_low = "b"
    elif s == "C": s_low = "c"
    elif s == "H": s_low = "h"
    elif s == "V": s_low = "v"
    elif s == "F": s_low = "f"
    elif s == "T": s_low = "t"
    else: s_low = "n"          # a number that we for now do not send
    
    if s_low != "n":
        radio.send(s_low)      # Send string - character in this context - on radio waves - default setting - channel and group 
        display.show(s_low)
        clear_disp()
        
def resp(s):
    if on_radio:
        send_on_radio(s)  # send character in lower case on radio unless its a number
    else:
        print(s)          # Send string - in this program only single characters used - on seriel port (USB)
        display.show(s)   # Local feedback on microbit display showing string
        clear_disp()      # Clear display until next event happens - Next event will not register until display is cleared


print("Hello World - Klar på den serielle")    # Ready
display.show(Image.HAPPY)
sleep(2000)
clear_disp()


while True:                                    # Forever - at leat until power off/reset - generate events on USB or radio
                                                                      
    if button_a.was_pressed():
        resp("A")

    if button_b.was_pressed():
        resp("B")
        
    if pin0.is_touched():
        resp("C")

    if pin1.is_touched():
        resp(str(random.randint(0, 9)))

    if pin2.is_touched():                       # Turn on/off transmission on radio via A+B at same time
        if on_radio:
            on_radio = False
            display.show(Image.SQUARE)
            sleep(200)
            display.show(Image.SQUARE_SMALL)
        else:
            on_radio = True
            display.show(Image.SQUARE_SMALL)
            sleep(200)
            display.show(Image.SQUARE)

    reading1 = accelerometer.get_x()
    sleep(20)
    reading2 = accelerometer.get_x()
     
    if reading1 > 500 and reading2 > 500:           # filtering out spikes with 2 readings
        resp("H")
    elif reading1 < -500 and reading2 < -500:
        resp("V")
       
    reading1 = accelerometer.get_y()
    sleep(20)
    reading2 = accelerometer.get_y()
    
    if reading1 > 500 and reading2 > 500:
        resp("F")
    elif reading1 < -500 and reading2 < -500 :
        resp("T")

    r = radio.receive()
    if r: print(r)
    
    
    
   
        
     
        
