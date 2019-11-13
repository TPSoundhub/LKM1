# M1Sc-VisSeriel.py - Show active serial ports so the one with microbit can be identified.
# Revison 1.0 12112019, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
# 
# Utility - Prints the active ports on PC/PI/Mac
# Simply run it in editor (Thonny) and see list of ports.
# If in doubt then do it without microbit connected frst and then a second time with the Microbit connected.
# Then it sould be obious what the name of the serial port the microbit is connected to.
# This name is then the one to be used in the program reading input from the microbit on the serial connection.
#
# Can identify this in other ways using ex a terminal programme like Terra Term but this depends on wheter you use PC, MAC or PI
# Using a terminal program on the other hand also right away can show you what the Micro bit is sending.
# BUT then you must set up the communication in the terminal to communicate with the baoudrate 115200
#
# On PC you can also use the window+x shortcut and go to "enhedshåndtering" to see active/inactive serial ports
#

import serial.tools.list_ports
print([comport.device for comport in serial.tools.list_ports.comports()])

