# M1Se-Filterinput.py - Sample code filtering input from MBs
# Revison 1.0 03122019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#
# This code is to illustrate filtering of inputs from different/selected Micro:Bits, as this has been a
# FAQ after introducing the KIT - and has been posted as one of the hidden challenges in previous code
# samples.
#
# This code code ignores input from all other micro:Bits than the specific two with the names given by the
# constants:
#
# relevant_sender_1         = "Knud-3    "
# relevant_sende_2          = "Knud 1    "
#
# Change these name to two names of MB's in your working group, and run the program and se what the result are.
# follw the code and experiment with inputs from the to MB, and learn the behaviour of the code.
# remember to set the port name to the correct one!
# you control the 'level' of information you get in the shell by printouts via the constants
#
# test_print_1
# test_print_2
#
# Settign both to False means NO printouts at all so no information - this is only for use when you understand ans trust
# the code. Test_print_2 = True and test_print_1 = True gives you the opportunity to follow the logic when sending input
# events from the two MBs. also setting the test_print-1 = True gives you printouts also for what is received including
# the timesouts so you can follw those as well
#
# In this way yu can make sure your code will not react to any radio transmission from any other MBs
# belonging to an other group.
#
# In this code no sound is played back - only printouts to indicate what to do as next step to use this
# code as a skeleton for building code that do specific stuff on specific inputs from specific MBs
#
# One improtant concept to understand is the difference between event and state. When I fell asleep it is an event - something happening
# at a specific moment and tranfering (me) from one state to another (awake to asleep)
#
# All inputs from the MB in module 1 is typical events. Something happning. The repetitive tilt inputs are though not
# tranformation from one state to another. Only the first incomming "V"/"v" tells about a transformation from
# 'not tilted or titled in another direction' to 'tilted to the left' Secondary "V"/"v"s just tells the tilt is still
# ongoing. You might wnat to differentiate between the two. This code contains an exsample on how to.
#
# The MB you have been given DO NOT send an event for when it is going from tilted to 'normal'/flat/level state! So a
# question/challenge was how to figure taht out if needed. And it is needed for figuring out the first incoming tilt, going from
# level state to tilted state in any direction. This code contains an exsample on how to do that. It implies a timeout on
# the reading input from MB. Previous implementations have just wainted forever on input from the MB. And the MB do not
# send anything if level and with constant light intensity, so your code on the receiving side can not do anything while waiting for input
# from the MB. That can be solved by a timeout on the reading. If timeout you know the MB have been level for a period.
#
# The "N"/"D"/"S" is events telling a transition between states: "Low light intensity", "Medium light intensity" and
# "High light intensity". Some of you want to know the state of the light when you receive another input so it can be
# combined for an 'intelliigent' condition for playing sound. Eg when tilt event arrive when dark then NO SOUND while
# sound is played on tilt when other light state. So Question/Challenge then is to remember light state for later use
# when light event is received. This code contains an example on how to do that. It simply is about keeping the light state
# in a global variable for later use - as you cannot ask the MB for the state when needed.
#
# Light states by the way fluctuate/is influenced naturaaly by hand approcing MB. So as such light events from MB that is
# used for operation by hand is not valid. So how to deal with that has also been a Question. This can simply be done
# by giving different MBs different roles in your product - you have at least 3 MBs in every group. You can then
# ignore light sensor input from the MB you use for operation by hand. This code contains example on how to do that using the
# unique names that are in each MB. The example in this code only use light sensor input from one MB and all other inputs
# from the second MB. Roles between MBs can of cource be done differently by modifying this code. And also be explanded with
# more MBs - this code only use two to illutrate principles.
#
# Go use this as insiration for your own code - go build stuff with it!
#
# Where the test_print_2 printouts are located you can insert code for specific actions on the filtered input.
#
#
import serial

#
# Definitiona, variables and constants. Note timeout set on the serial to 1 sec.
# Meaning if nothing is read/incomming on the serial port for one second then the readline returns without a valid value in rc and who
# which means the MBs have been steady for a while. Can lots of remote MBs in the room influence this? And how to avoid this is a
# next level challenge :-) which we for now do not dig into....
#

ser = serial.Serial(timeout=1)
ser.baudrate = 115200
ser.port = "COM5"

test_print_1 = False
test_print_2 = True


light_events              = ["N","D","S","n","d","s"]                  # Low, normal and high intensity just named like the event from MB in this case
current_light_state       = None                                   # Set the initial light state to None as we do not know the state yet as we have not been given an light event from the MB yet 

tilt_events               = ["H","V","F","T","h","v","f","t"]      # tilt events as they arrive from MB the others for tilt in speicfied direction
current_tilt_state        = None                                   # Set the initial tilt state to None as we do not know the state yet as we have not been given a tilt event from the MB yet
                                                                   # when getting tilt event we just set the state to the name of the incomming event in this code
                                                                   # and when deducing it is not tilted anymore (timeout from reading MB input) then it is set to "None".

relevant_sender_1         = "Knud-3    "
relevant_sende_2          = "Knud 1    "


#
# Definition of functions
# The receive_char function you have seen  before slightly modified to return None for RC and Who in the case of timeout
# Then a new function that filter events so irrelevant MBs are filtered out and only light commands accepted from one MB
# None is returned if no relevant event is received.
# This should be modified to your need
#

def receive_char():
    microbitdata = str(ser.readline())
    if test_print_1: print(len(microbitdata),microbitdata)
    if len(microbitdata)>3:
        return microbitdata[2], microbitdata[4:14]
    else:
        return None, None

def relevant_event(rc,who):
    if (who == "Knud-3    ") and (rc in light_events):
        return rc
    elif (who == "Knud 1    ") and (rc not in light_events):
        return rc
    else:
        return None
    

#
# Main code
#


ser.open()


while True:
    rc,who = receive_char()
    if rc == None: # Nothing received - taht is a timeout on the serial port then
        if test_print_1: print("timeout - nothing received")
        current_tilt_state = None  # not tilted as we have a timeout from MB reading.
    else:  # Something received
        if test_print_1: print("received character:",rc,"from:",who, "String with the lenght",len(who))
        event = relevant_event(rc,who)
        if event!=None:
            if event in tilt_events:
                if event == current_tilt_state:
                    if test_print_2: print("Do repeated tilt stuff if any",who,event)
                else:
                    if test_print_2:
                        print("Do tilt stuff on first tilt event in specifik direction and set tilt state",who,event)
                        print("The code for tilt can then take current light state into accout if you want", current_light_state)
                    current_tilt_state = event
            elif event in light_events:
                 if test_print_2: print("Do light stuff and remember current light state for use elsewhere",who,event)
                 current_light_state = event
            else:  # Other input than tilt and light
                if test_print_2:
                    print("Do stuff on other input than tilt and light",who,event)
                    print("The code for other inputs can then take current light state into accout if you want", current_light_state)

    
