# Basic event maker for LYDKit project P1 winter 2019. SSG, SHD, Herningsholm, Skanderborg - sponsered by Region MidtJylland
#
# Version 14 september 2019, Knud Funch SHD (used in HH - where tha one from 13th are used in SSG
# - Changed range in light measure for 'Day' to 40 to 180 instead of 50 to 150 as is seems to fit better 
#
# Version 13 september 2019, Knud Funch SHD
# - Added name for identification
# - Added light intensity reading. So Night, Day and sunshine can be simulated and used in project
#
# Version 12 september 2019, Knud Funch SHD
# - Added basic filtering on accelerometer input - removing spike readings
#
# Version 9th september 2019, Knud Funch SHD
# - first version with button and tilt plus radio.
#
# Microbit functionality in short:
#
# Send string "Hello world ..." on serial USB and make Happy face on LEDs when powerup
# Send characters on serial USB when sensors/buttons are triggered
#
# - "A", "B" when a/b key is pressed - plus "A" "B" on local display - Once pr press
# - "C" when pin 0 is activated - repetitive as long as pin 0 is active whith 500ms spacing
# - "0" - "9" randomly selected when pin 1 is active - repetivite 500ms spacing
# - "V" - when tilted to left   - repetitive 500ms spacing
# - "H" - When tilted to right  - repetitive 500ms spacing
# - "F" - when tilted forward   - repetitive 500ms spacing
# - "T" - when tilted backwards - repetitive 500ms spacing
# - "D" - when light intensity goes from outside range into range between 40 and 180. (Skift til Dag)
# - "N" - when light intensity goes from above to below 40.                           (Skift til Nat)
# - "S" - when light intensity goes from below to above 180.                          (Skift til Solskin>Dag)
#
# - Switch mode between sending on radio ws sending on serial when pin 2 is active
#    - small square followed by big square  -> Radio tansmission from remote location
#    - big square followed by small square  -> Serial transmission local connected via USB
# If transmisson on radio then feedback on LED are in small letters "a","b" etc..
#     - and so is the character transmitted.
#     - Digits not transmitted - so no action on pin 1 when in radio transmission mode.
#
# If anything is received on radio the received character is sent on serial USB. No feedback on LEDs
# Feedback is given on the remote MicroBit
#
# All characters are follwed by <name> for unique identification
#
from microbit import *
import random
import radio

navn = "Asger     "        # 10 characters to identify MB - use name on beholder

radio.on()                 # Turn on radio module so it can send and receive messages - do use some extra power!
on_radio = False           # Global variable to decide whether or not to send character on radio
current_lev = " "          # Initialise current light level to value not sent. Then it will be sent at first reading.

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
    elif s == "N": s_low = "n"
    elif s == "D": s_low = "d"
    elif s == "S": s_low = "s"
    else: s_low = "z"          # a character that we for now do not send meaning nothing to be sent
    
    if s_low != "z":
        sognavn=s_low+"-"+navn
        radio.send(sognavn)   # Send string - eventcharacter plus name - on radio waves - default setting - channel and group 
        display.show(s_low)
        clear_disp()
        
def resp(s):
    if on_radio:
        send_on_radio(s)  # send character in lower case on radio unless its a number
    else:
        print(s,navn)     # Send string - in this program only single characters used - on seriel port (USB)
        display.show(s)   # Local feedback on microbit display showing string
        clear_disp()      # Clear display until next event happens - Next event will not register until display is cleared



print("Hello World - Klar på den serielle ",navn)    # Ready

display.show(Image.HAPPY)
sleep(2000)
clear_disp()


while True:                  # Forever - at least until power off/reset - generate events on USB or radio
                                                                      
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

    light=display.read_light_level()
    if light < 40:
        new_lev="N"
    elif light > 180:
        new_lev="S"
    else:
        new_lev="D"
        
    if new_lev != current_lev:
        current_lev=new_lev
        resp(current_lev)

    r = radio.receive()
    if r: print(r)
    
    
    
   
        
     
        
