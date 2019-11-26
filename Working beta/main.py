print("YOU ARE RUNNING AN UNTESTED COPY OF THE MAIN CODE!")
accept = input("Do you accept the risk? ")
if accept != 'Yes':
	exit()
#716 Demo-bot code for RaspberryPi 3b+, updated 11/22/19 by Jacob Ellington
import time
import math
import pygame
import os
from pygame.locals import *
global loop, rightDrive, leftDrive, deadMan, controller, CtrlType, ShootTimer
import sys
import board
import digitalio
loop = 0
deadMan = False #starts assuming deadman is active, meaning robot cannot move
black = (0,0,0)
ShootTimer = 0
white = (255,255,255)
red = (255,0,0)
blue = (57,17,184)
yellow = (224,213,4)
display_width = 1280
display_height = 720
#-----Start Output Mappings-----
RightDrive = 0
LeftDrive = 1
ShootWheel = 2
FeedWheel = 3
TableMotor = 4
#---
idle = 0 #0.025
shootIdle = 0.025
allowShootSpeedChange = True
ShootPower = 0.99 #starting shoot power
FeedPowerInit = 0.5
TablePower = 0.99
DrivePower = 0.99
ShootDelay = 1.8 #Seconds to allow shooter to spool up
xDeadZone = 0.16
yDeadZone = 0.16
MotorDeadZone = 0 #0.025
#-----End Output Mappings-------
dPadReleased = True
CtrlType = 'wireless' #assumes we are using xbox wireless controls
verbose = False
for x in sys.argv:
	if x == '--verbose':
		verbose = True
	elif x == '--help':
		os.system("cat /home/pi/Robotics/.MainHelp.md")
		exit()
	elif x == '--wired':
		CtrlType = 'wired'
	elif x == '--fixed-speeds':
		allowShootSpeedChange = False
	elif x == '--test-interfaces':
		print ("Initiating Adafruit Interface Test Suite...")
		try:
			import board
			import digitalio
			import busio
			# Try to great a Digital input
			pin = digitalio.DigitalInOut(board.D4)
			print("Digital IO ok!")
			# Try to create an I2C device
			i2c = busio.I2C(board.SCL, board.SDA)
			print("I2C ok!")
			# Try to create an SPI device
			spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
			print("SPI ok!")
			print("done! All I/O reports OK")
			InterfaceQuestion = input("Proceed with Robot Operations? ")
			if InterfaceQuestion == 'yes':
				print("Launching...")
				pass
			else:
				print('Quitting. (you needed to type "yes" to to continue)')
				exit()
		except(FileNotFoundError, RuntimeError):
			print("One or more interfaces failed during testing. Abort.")
			exit()
print ("Verbose Mode: ", verbose)
print ("Control Type: ", CtrlType)
#robotDisplay = pygame.display.set_mode((50, 70))
if CtrlType == 'wireless': os.system('sudo ./CheckCtrl.py') #idk if this will hang the code lol
from adafruit_servokit import ServoKit
board = ServoKit(channels=16)
pygame.init()
robotDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Demo Bot')
def Controls_init():
	global CtrlType, controller, controllerX, rStickDown, controllerY, rTrigger, lTrigger, rBumper, lBumper, bButton, verbose, xButton
	controller = pygame.joystick.Joystick(0)
	controller.init()
	if CtrlType == 'wireless': #default mappings for wireless controller
		controllerY = -1* (controller.get_axis(3))
		controllerX = controller.get_axis(2)
		rTrigger = controller.get_axis(4)
		lTrigger = controller.get_axis(5)
		rBumper = controller.get_button(6)
		lBumper = controller.get_button(6)
		bButton = controller.get_button(1)
		xButton = controller.get_button(3)
		rStickDown = controller.get_button(14)
		dPadUp = 0 #Need Value!
		dPadDown = 0 #Need Value!
	elif CtrlType == 'wired': #default mappings for Wired controller
		controllerY = -1* (controller.get_axis(4))
		controllerX = controller.get_axis(3)
		rTrigger = controller.get_axis(5)
		lTrigger = controller.get_axis(2)
		rBumper = controller.get_button(5)
		lBumper = controller.get_button(4)
		bButton = controller.get_button(1)
		xButton = controller.get_button(2)
		rStickDown = 0 #Need Value!
		dPadUp = 0 #Need Value!
		dPadDown = 0 #Need Value!
	else:
		print("Critical Error")
		if verbose:
			print("Error: a control scheme has not been assigned to the CtrlType variable. Halt. Got Control Scheme: ", CtrlType)
		pygame.quit()
		exit()
	if verbose: print("Raw Inputs (x,y) are: {0}, {1}".format(controllerX, controllerY))
	if abs(controllerY) <= yDeadZone:
		controllerY = 0
	if abs(controllerX) <= xDeadZone:
		controllerX = 0

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()
def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',55)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	robotDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
def sub_message_display(text): #TODO: fix strobing issue
	medText = pygame.font.Font('freesansbold.ttf',30)
	TextSurf, TextRect = text_objects(text, medText)
	TextRect.center = ((display_width/2),(display_height/3))
	robotDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
def loopDrive():
	global controllerY, controllerX
	if verbose: print ("Processed X, Y= ", controllerX, controllerY)
	leftPower = (controllerY - controllerX) + idle
	rightPower = (controllerY + controllerX) + idle
	if rStickDown == 0:
		leftPower = leftPower * DrivePower
		rightPower = rightPower * DrivePower
	elif rStickDown == 1:
		if verbose: print("Speed Override ON!")
		sub_message_display("Speed Override ON")
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
	if verbose: print ("Motor Conditions (l,r):", leftPower, rightPower)
def shooter():
	global rTrigger, ShootTimer, FeedPower
	FeedPower = (FeedPowerInit * ShootPower) + 0.1
	if FeedPower >= 1: FeedPower = 0.99
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
		board.continuous_servo[FeedWheel].throttle = shootIdle
		board.continuous_servo[ShootWheel].throttle = shootIdle
def eventHandler():
	global deadMan, CtrlType, ShootPower, dPadReleased
	deadMan = True
	for event in pygame.event.get(): # User did something.
		if event.type == pygame.QUIT: # If user clicked close.
			quit()
		elif event.type == KEYDOWN:
			if event.key == k_SPACE:
				os.system("./Estop.py")
				pygame.quit()
				exit()
			if event.key == K_ESCAPE:
				pygame.quit()
				if verbose: print("A keyboard request to exit has been registered. Halt.")
				exit()
	if bButton == 1:
		exit()
	if xButton == 1:
		os.system("sudo shutdown now") #cut power immediatley
	if lBumper == 1:
		deadMan = False
	if (dPadUp == 0) and (dPadDown == 0): dPadReleased = True
	if allowShootSpeedChange and dPadReleased = True:
		if dPadUp == 1 and (ShootPower <= 0.99):
			ShootPower += 0.1
			dPadReleased = False
		elif dPadDown == 1 and (ShootPower >= 0.15):
			ShootPower -= 0.1
			dPadReleased = False
def Stopped():
	if deadMan == True:
		print("Stopped!")
		board.continuous_servo[RightDrive].throttle = idle
		board.continuous_servo[LeftDrive].throttle = idle
		board.continuous_servo[TableMotor].throttle = idle
		board.continuous_servo[ShootWheel].throttle = shootIdle
		board.continuous_servo[FeedWheel].throttle = shootIdle
		eventHandler()
		robotDisplay.fill(red)
		message_display('System E-Stopped. Hold Left Bumper.')
		if verbose: print("Emergency Stopped! Hold the Left Bumper on the xbox controller to resume normal operations.")
		time.sleep(0.1)
def Running():
	if deadMan == False:
		eventHandler()
		loopDrive()
		shooter()
		robotDisplay.fill(yellow)
		message_display('716 DemoBot Enabled  :-)')
while True:
	time.sleep(0.001)
	Controls_init()
	eventHandler()
	Running()
	Stopped()
