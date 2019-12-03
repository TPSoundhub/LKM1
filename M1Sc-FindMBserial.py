# M1Sc.py - Find Micro:Bit on serial port
# Revison 1.1 25112019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
# - Extra set of port names for MAC
# Revison 1.0 12112019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
# 
# Program to find a serial port with a serial communication device connected (Micro:Bit) either on PC or PI
# Not bullet proof! If more serial devices connected or connected more than 10 (logical and over time) it can be out of range
# 
# Note - After found device it simply waits until something arrives on serial and then print char from received string in shell.
#      - If it should not wait then change timeout in ser definition first in programme. Then the programme can check for other events.
#
# Try it out!
# Combine with music/sound playing from pygame and build stuff!
#
import serial

ser = serial.Serial(timeout=None)                        # "ser" beeing defined to represent "serial.Serial(timeout=None" later in programme.
ser.baudrate = 115200                                    # just like initials KFU can be used in an proganization to represent my name "Knud Funch"
                                                         # That is just to make coding easier as you can avoid to type the long function names.
                                                         # BUT - be carefull as it becomes more and our own language and might not be as easy to read and
                                                         # understand for 3rd parties, and good programming practice includes make it easy to read.

test_prt = True                                          # Another good practice can be to add code that helps in testing, and make it easy to turn on/off
                                                         # Here a flag to turn test printouts on/off during development and testing of code
                                                         # try to set it to False and run program and see the difference

ports_on_pc = ["COM0","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9"]
ports_on_pi = ["/dev/ttyACM0","/dev/ttyACM1","/dev/ttyACM2","/dev/ttyACM3","/dev/ttyACM4",
               "/dev/ttyACM5","/dev/ttyACM6","/dev/ttyACM7","/dev/ttyACM8","/dev/ttyACM9"]
ports_on_mac1 = ["/dev/tty.usbmodem14102","/dev/tty.usbmodem14202","/dev/tty.usbmodem14302","/dev/tty.usbmodem14402","/dev/tty.usbmodem14502",
                "/dev/tty.usbmodem14602","/dev/tty.usbmodem14702","/dev/tty.usbmodem14702","/dev/tty.usbmodem14802","/dev/tty.usbmodem14902"]
ports_on_mac2 = ["/dev/cu.usbmodem14102","/dev/cu.usbmodem14202","/dev/cu.usbmodem14302","/dev/cu.usbmodem14402","/dev/cu.usbmodem14502",
                "/dev/cu.usbmodem14602","/dev/cu.usbmodem14702","/dev/cu.usbmodem14702","/dev/cu.usbmodem14802","/dev/cu.usbmodem14902"]
def find_port(computer):
    port_number = None

    for p in range(0,10):
        try:
            port_ok = True
            if computer == "PC": port_name = ports_on_pc[p]
            elif computer == "PI": port_name = ports_on_pi[p]
            elif computer == "MAC1": port_name = ports_on_mac1[p]
            elif computer == "MAC2": port_name = ports_on_mac2[p]
            else: port_name = "unknown"
            ser.port = port_name
            ser.open()
            if port_ok:                                   # no exception occured in call ser.open() meaning dev connected on port!!
                port_number = p                           # no need to seek further and the loop is stopped by a break and
                break                                     # then port_name is valid on return and port is already open and ready

        except serial.SerialException:                    # ser.open() can not execute meaning no dev on port - so exception occur!!
            if test_prt: print("No Micro:Bit found on: ", port_name)    
            port_ok = False
    return port_number, port_name


port_found = False
p,n = find_port("PC")
if p == None: p,n = find_port("PI")                       # did not find on PC if None is returned so then try to find on PI to make it work on both without changing code
if p == None: p,n = find_port("MAC1")                     # did not find on MAC with name 1 (tty) if none is returned so then try to find on MAC with name 2(cu) to make it work on all 3
if p == None: p,n = find_port("MAC2")                     # did not find on MAC with name 2 if none is returned

if p != None:
    port_found = True
    print("Device found on: ",n," - and port is ready for communicaiton - Press a button on Micro:Bit to see it is the one") 
else:
    print("Could not find Micro:Bit. Program ends!")


while port_found:                                         # This is done forever if port is found. What if Micro:Bit is detached? See challenge 1 in comments after code
    rc = str(ser.readline())                              #
    if test_prt: print(rc)                                # Micro:Bit sends a strnig with more charaters and the one wee seek for as input event are number 2
    rc = rc[2]                                            # when running from within Thonny. See challenge number 2 below 
    print(rc)                                             # 
    
ser.close()

# Challenge 1: Try to remove MicroBit from port after code is up runing - what happens? Can that be dealt with in code? How?
#              This might not be the first challenge to dig into though! Better to build stuff that reacts on input from Micro:Bit as next step (more fun) :-)
# Challenge 2: Try to run this program from command line (CLI) on the PI and see what number the wanted character is placed on in that case.
#              Change program to work from CLI. Can you find a way to make the code work from both CLI and within Thonny (GUI) without change?
#