#uses linux l2ping module to ensure connectivity with controller at all times
import os
import time
import pygame
import math
import psutil
global SpawnEstop
white = (255,255,255)
width = 1920
height = 1080
x = width / 2
y = height / 2
SpawnEstop = 0
while True:
	ping = os.system("l2ping -c 1 5C:BA:37:E5:A7:8D")
	if ping == 0:
		SpawnEstop = 0
		pygame.quit()
		if ("./Estop" in (p.name() for p in psutil.process_iter())):
			print("found Estop")
		else:
			print("cant find it")
	else:
		pygame.init()
		xboxMissing = pygame.image.load('NoController.png')
		robotDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		robotDisplay.fill(white)
		robotDisplay.blit(xboxMissing, (x,y))
		pygame.display.update()
		if SpawnEstop <=3: #Spawns several instances for speed and reduncancy
			os.system("python3 /home/pi/Robotics/Estop.py")
			SpawnEstop += 1

