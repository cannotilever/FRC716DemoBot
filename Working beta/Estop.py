#!/usr/bin/python3
#Ain't pretty but shuts down everything
#has as little logic as possible to run faster than main loop
from adafruit_servokit import ServoKit
from pygame.locals import *
board = ServoKit(channels=16)
while True: #not putting in a delay is intentional, don't care about CPU load bc GIL
     board.continuous_servo[0].throttle = 0
     board.continuous_servo[1].throttle = 0
     board.continuous_servo[2].throttle = 0
     board.continuous_servo[3].throttle = 0
     board.continuous_servo[4].throttle = 0
     board.continuous_servo[5].throttle = 0
     board.continuous_servo[6].throttle = 0
     board.continuous_servo[7].throttle = 0
     board.continuous_servo[8].throttle = 0
     board.continuous_servo[9].throttle = 0
     board.continuous_servo[10].throttle = 0
     board.continuous_servo[11].throttle = 0
     board.continuous_servo[12].throttle = 0
     board.continuous_servo[13].throttle = 0
     board.continuous_servo[14].throttle = 0
     board.continuous_servo[15].throttle = 0
     print("stopped everything")

