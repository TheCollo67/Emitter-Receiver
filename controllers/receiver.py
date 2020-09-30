# Import modules
from controller import Robot
from controller import Motor
from controller import DistanceSensor
from controller import Receiver

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

# Receiver setup

receiver = robot.getReceiver('receiver')
receiver.enable(1)
receiver.setChannel(COMM_CHANNEL)
message_printed = 0
isTooClose = False

# Main 

while robot.step(TIMESTEP) != -1:
    leftSpeed = ROBOT_SPEED
    rightSpeed = ROBOT_SPEED

    # Read sensors
    for i in range(2):
        if ds[i].getValue() > 500.0:
            leftSpeed += ROBOT_SPEED
            rightSpeed -= ROBOT_SPEED
            if ds[i].getValue() > 900:
                leftSpeed += ROBOT_SPEED
                rightSpeed -= ROBOT_SPEED
                if ds[i].getValue() > 950:
                    isTooClose = True
    if isTooClose == True:
        leftSpeed = 0
        rightSpeed = ROBOT_SPEED * -3.0
        isTooClose = False
    
    # Sensor data action
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    
    # Receiver 
    
    if receiver.getQueueLength() > 0:
	
        message = (receiver.getData())
        if message_printed !=1:
            print(f"Communicating: Received {message.decode('utf-8')}\n")
            message_printed = 1
    else:
        if message_printed !=2:
            print("Communication broken!")
            message_printed = 2
	    
    receiver.nextPacket()
    
    pass