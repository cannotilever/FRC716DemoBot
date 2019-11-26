#!/usr/bin/python3
#WARNING: CURRENTLY UNUSABLE AS NO MAC ADDRESS IS SUPPLIED TO THE L2PING FUNCTION
import os
import time
from adafruit_servokit import ServoKit
board = ServoKit(channels=16)
cutoff = float(60) #maximum allowable trip time (in ms) between the robot and controller
eStop = False
loopCounter = 0
def main():
	pingR = os.system("sudo l2ping -c 0") #TODO add MAC address
	global eStop
	for word in pingR.split():
		if 'ms' in word: pingTime = word
	pingTime = pingTime.replace(pingTime[-1], '')
	pingTime = pingTime.replace(pingTime[-1], '')
	pingTimeF = float(pingTime)
	print(type(pingTimeF))
	if pingTimeF <= cutoff:
		eStop = False
	else:
		eStop = True
def stopper():
	for i in range(0,16):
		board.continuous_servo[i].throttle = 0
		print("Stopped!")
while True:
	startT = time.time()
	global loopCounter
	loopCounter += 1
	if eStop:
		stopper()
		if loopCounter == 60000:
			loopCounter = 0
			main()
	else: main()
