# Import modules 
from controller import Robot
from controller import Motor
from controller import DistanceSensor
from controller import Emitter
import struct

# Create a robot instance
robot = Robot()

# Declare constants
TIMESTEP = int(robot.getBasicTimeStep())
COMM_CHANNEL = 14
ROBOT_SPEED = 5.0

# Sensors setup

ds = []
dsNames = ['ds0', 'ds1']
for name in dsNames:
    ds.append(robot.getDistanceSensor(name))
for i in range(2):
    ds[i].enable(TIMESTEP)

# Motors setup

wheels = []
wheelsNames = ['left wheel motor', 'right wheel motor']
for name in wheelsNames:
    wheels.append(robot.getMotor(name))
for i in range(2):
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

# Emitter setup

emitter = robot.getEmitter('emitter')
emitter.setChannel(COMM_CHANNEL)
message = 'Hello!'
isTooClose = False

# Main 

while robot.step(TIMESTEP) != -1:
    leftSpeed = ROBOT_SPEED
    rightSpeed = ROBOT_SPEED

    # Read sensors
    for i in range(2):
        if ds[i].getValue() > 500.0:
            leftSpeed -= ROBOT_SPEED
            rightSpeed += ROBOT_SPEED
            if ds[i].getValue() > 900:
                leftSpeed -= ROBOT_SPEED
                rightSpeed += ROBOT_SPEED
                if ds[i].getValue() > 950:
                    isTooClose = True
    if isTooClose == True:
        leftSpeed = ROBOT_SPEED * -2.0
        rightSpeed = 0
        isTooClose = False
    
    # sensor action data
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    
    # emitter action 
    emitter.send(message.encode('utf-8'))
    
    pass