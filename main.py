#716 Demo-bot code for RaspberryPi 3b+, updated 9/10/19 by Jacob Ellington
import time
import math
import pygame
import os
from adafruit_servokit import ServoKit
from pygame.locals import *
global loop, rightDrive, leftDrive, deadMan, controller, CtrlType
import sys
loop = 0
deadMan = False #starts assuming deadman is active, meaning robot cannot move
board = ServoKit(channels=16)
black = (0,0,0)
ShootTimer = 0
white = (255,255,255)
red = (255,0,0)
blue = (57,17,184)
yellow = (224,213,4)
pygame.init()
pygame.joystick.init()
display_width = 1280
display_height = 720
#-----Start Output Mappings-----
RightDrive = 0
LeftDrive = 1
ShootWheel = 2
FeedWheel = 3
TableMotor = 4
#---
idle = 0
ShootPower = 0.99
FeedPower = 0.99
TablePower = 0.99
DrivePower = 0.99
ShootDelay = 2 #Seconds to allow shooter to spool up
#-----End Output Mappings-------
CtrlType = xbone #assumes we are using xbox 1 controls
verbose = False
try:
	if sys.argv[1] == '360':
		CtrlType = xb360
		print("Started Code with Xbox360 Controls")
except(IndexError):
	print("Assuming Xbox One control scheme")
	pass
try:
	if (sys.argv[1] == 'verbose') or (sys.argv[2] == 'verbose'):
		verbose = True
except(IndexError):
	pass
print ("Verbose Mode: ", verbose)
#robotDisplay = pygame.display.set_mode((50, 70))
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Demo Bot')
def Controls_init():
	controller = pygame.joystick.Joystick(0)
        controller.init()
	if CtrlType == xbone: #default mappings for wireless controller
	controllerY = -1* (controller.get_axis(3))
	controllerX = controller.get_axis(2)
	rTrigger = controller.get_axis(4)
	lTrigger = null #Need Value!
	rBumper = null #Need Value!
	lBumper = controller.get_button(6)
	bButton = controller.get_button(1)
	if CtrlType == xb360:
		print("Not Yet Implimented!")
		exit()
	else:
		print("Critical Error")
		if verbose:
			print("Error: a control scheme has not been assigned to the CtrlType variable. Halt.")
		pygame.quit()
		exit()
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',55)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    robotDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
def loopDrive():
	global controllerY, controllerX
	if verbose: print ("X, Y= ", controllerX, controllerY)
	leftPower = (controllerY + controllerX)
	rightPower = (controllerY - controllerX)
	if leftPower >= 1:
		leftPower = 0.99
	if rightPower >= 1:
		rightPower = 0.99
	if leftPower <= -1:
		leftPower = -0.99
	if rightPower <= -1:
		rightPower = -0.99
	board.continuous_servo[LeftDrive].throttle = leftPower
	board.continuous_servo[RightDrive].throttle = rightPower
	if verbose: print ("Motor powers :", leftPower, rightPower)
def shooter():
	global rTrigger
	if rTrigger >= 0.5:
		if verbose:
			print("Shooter System Activated!")
	board.continuous_servo[ShootWheel].throttle = ShootPower
		if (time.time() - ShootTimer) > ShootDelay:
			board.continuous_servo[TableMotor].throttle = TablePower
			board.continuous_servo[FeedWheel].throttle = FeedPower
	else:
		ShootTimer = time.time()
		board.continuous_servo[TableMotor].throttle = idle
		board.continuous_servo[FeedMotor].throttle = idle
		board.continuous_servo[ShootMotor].throttle = idle
def eventHandler():
	global deadMan
	deadMan = True
	for event in pygame.event.get(): # User did something.
		if event.type == pygame.QUIT: # If user clicked close.
			quit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE or K_SPACE:
				pygame.quit()
				if verbose: print("A keyboard request to exit has been registered. Halt.")
				exit()
	if bButton == 1:
		exit()
	if lBumper == 1:
		deadMan = False
	ping = os.system("l2ping -c 1 5C:BA:37:E5:A7:8D")
	if ping !=0:
		deadMan = True
def Stopped():
	if deadMan == True:
		print("Stopped!")
		board.continuous_servo[RightDrive].throttle = idle
		board.continuous_servo[LeftDrive].throttle = idle
		board.continuous_servo[TableMotor].throttle = idle
		board.continuous_servo[ShootMotor].throttle = idle
		board.continuous_servo[FeedMotor].throttle = idle
		eventHandler()
		robotDisplay.fill(red)
		message_display('System Halted. Hold Deadman.')
		if verbose: print("Emergency Stopped! Hold the Left Bumper on the xbox controller to resume normal operations.")
		time.sleep(0.1)
def Running():
	if deadMan == False:
		eventHandler()
		loopDrive()
		robotDisplay.fill(yellow)
		message_display('716 Demo')
while True:
	time.sleep(0.01)
	Controls_init()
	eventHandler()
	Running()
	Stopped()
