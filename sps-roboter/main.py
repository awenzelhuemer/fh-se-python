#!/usr/bin/env pybricks-micropython

import random

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor, GyroSensor
from pybricks.parameters import Port, Color, Button, Stop
from pybricks.robotics import DriveBase

from pybricks.tools import StopWatch

import config

# Initialize the EV3 brick.
brick = EV3Brick()

# sensors
colorSensor = ColorSensor(Port.S1)
infraredSensor = InfraredSensor(Port.S3)  
gyroSensor = GyroSensor(Port.S2)

# motors
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.D)
robotDrive = DriveBase(leftMotor, rightMotor,
                       config.WHEEL_DIAMETER, config.AXLE_DISTANCE)
killMotor = Motor(Port.B)

def init():
    # print('--init--')
    killMotor.run_until_stalled(-120)
    gyroSensor.reset_angle(0)
    
def stop():
    robotDrive.stop()

# reads the color to destroy
def getColor(ignoreNone = True):
    # print('--getColor--')
    color = 'None'
    old_color = 'None'
    detectColor = True
    # print('ignore Color none:', ignoreNone)
    while detectColor:
        color = colorSensor.color()
        if color == old_color and (ignoreNone or color != None) and color != Color.BLACK:
            detectColor = False
            return color
        else:
            old_color = color

    return color


def destroy(color):
    # print('--destroy--')
    # move the motor to destroy the ballon

    shouldDestroy = getColor(ignoreNone=True) == color

    if shouldDestroy:
        killMotor.run_time(1000, 700, Stop.HOLD, True)
        killMotor.run_until_stalled(-120)
    
    return shouldDestroy

def turn90Deg(right = True):
    # print('--turn90Deg--')
    right_angle = config.ANGLE
    if not right:
        right_angle = right_angle * -1
    
    gyroSensor.reset_angle(0)
    remaining_turn = right_angle
    while True:
        robotDrive.turn(remaining_turn)
        remaining_turn = right_angle + gyroSensor.angle() # When turning right the gyro counts down
        if -1 < remaining_turn < 1:
            break
    gyroSensor.reset_angle(0)

def driveToColor():
    # print('--driveToColor--')
    robotDrive.drive(config.FORWARD_MOVEMENT_SPEED_SLOW, 0)
    while True:
            scanned_color = getColor(ignoreNone=True)
            dist = infraredSensor.distance()
            if dist > config.IRSENSOR_MAX_DISTANCE_TO_GROUND:
                robotDrive.straight(config.BACKWARD_MOVEMENT_SPEED)
                turn90Deg(right=True)
                robotDrive.drive(config.FORWARD_MOVEMENT_SPEED_SLOW, 0)
            if scanned_color != None and scanned_color != Color.BLACK:
                stop()
                break

def driveToNextBallon(color):
    killCount = 0

    turn90Deg(right=True) # Right from the start the ballons will be directly in front of the robot
    driveToColor() # The balloons will be right in front of the robot
    if destroy(color): # Check if there is a balloon we want to sting
        killCount = killCount + 1
        print('kill count: ' + str(killCount))
    robotDrive.straight(-50) # Back of since we will be to close to the balloons
    turn90Deg(right=True)

    # killCount < 4
    while True:
        dist = infraredSensor.distance()
        if dist > config.IRSENSOR_MAX_DISTANCE_TO_GROUND:
            robotDrive.straight(config.BACKWARD_MOVEMENT_SPEED)
            turn90Deg(right=True)
        robotDrive.straight(config.FORWARD_MOVEMENT_SPEED_SLOW)
        turn90Deg(right=False)
        driveToColor()
        if destroy(color):
            killCount = killCount + 1
            print('kill count: ' + str(killCount))
        robotDrive.straight(config.BACKWARD_MOVEMENT_SPEED)
        turn90Deg(right=True)

init()
driveToColor()
targetColor = getColor(ignoreNone=False)

brick.screen.print('Target: ' + str(targetColor))
print('Target: ' + str(targetColor))

driveToNextBallon(targetColor)

# finish
brick.speaker.beep(duration=400)