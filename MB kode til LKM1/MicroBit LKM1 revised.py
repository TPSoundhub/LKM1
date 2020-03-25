from microbit import *
import radio

#       0123456789   - Must be 10 characters long
navn = "LM1-1     "        # 10 characters to identify MB - use name on beholder

radio.on()                 # Turn on radio module so it can send and receive messages - do use some extra power!
on_radio = False           # Global variable to decide whether or not to send character on radio
local_connected = True
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
    elif s == "P": s_low = "p"
    elif s == "I": s_low = "i"
    else: s_low = "z"          # a character that we for now do not send meaning nothing to be sent
    
    if s_low != "z":
        sognavn=s_low+"-"+navn
        radio.send(sognavn)   # Send string - eventcharacter plus name - on radio waves - default setting - channel and group 
        display.show(s_low)
        clear_disp()
        
def resp(s):
    if local_connected:
        print(s,navn)     # Send string - on seriel port (USB)
        display.show(s)   # Local feedback on microbit display showing string
        clear_disp()      # Clear display until next event happens - Next event will not register until display is cleared
    else:
        send_on_radio(s)  # send character in lower case on radio unless its a number

def display_current_mode(lc):
    if lc:
        display.show(Image.SQUARE_SMALL)
    else:
        display.show(Image.SQUARE)


def check_mode_shift():
    global local_connected
    both_pressed = button_a.is_pressed() and button_b.is_pressed()
    if both_pressed:
        display_current_mode(local_connected)
        sleep(3000)
        display.clear()
        both_pressed = button_a.is_pressed() and button_b.is_pressed()
        if both_pressed:  # still after 3 sec
            if local_connected: local_connected = False
            else: local_connected = True
            display_current_mode(local_connected)
            sleep(3000)
            display.clear()


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
        resp("P")

    if pin2.is_touched():
        resp("I")

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

    check_mode_shift()
    
    if local_connected:
        r = radio.receive()
        if r: print(r)

        