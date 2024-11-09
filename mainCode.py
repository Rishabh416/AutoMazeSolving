# WORKING WITH INPUT MAZE

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
left_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=97)
drive_base.use_gyro(True)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 'E', 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 'S':
            start = i, j

print(start)

queue = [start]
parents = {start: None}

while queue:
    # current position
    x, y = queue.pop(0)
    
    # if the exit is found
    if maze[x][y] == 'E':
        path = []
        current = (x, y)
        while current is not None:
            path.append(current)
            current = parents[current]  
        path.reverse()  
    
    # mark visited cells
    if maze[x][y] == 0:
        maze[x][y] = 2

    for directionX, directionY in directions:
        newX, newY = x + directionX, y + directionY
        
        # check for valid path (it is within maze boundaries (length of array), next cell is 0 or E)
        if 0 <= newX < len(maze) and 0 <= newY < len(maze[0]) and (maze[newX][newY] == 0 or maze[newX][newY] == 'E'):
            if (newX, newY) not in parents:
                queue.append((newX, newY))
                parents[(newX, newY)] = (x, y)  

hub.imu.reset_heading(0)

def normalize_yaw(yaw_angle):
    # Normalize to the range -180 to 180 degrees
    normalized_yaw = (yaw_angle + 180) % 360 - 180
    return int(normalized_yaw)


def doubleTurn(heading, direction):
    yawAngle = normalize_yaw(hub.imu.heading())
    if direction == "right": 
        while not((heading - 40) <= yawAngle <= (heading + 40)): 
            drive_base.drive(0, 90)
            yawAngle = normalize_yaw(hub.imu.heading())
        while not((heading - 2) <= yawAngle <= (heading + 2)): 
            drive_base.drive(0, 50)
            yawAngle = normalize_yaw(hub.imu.heading())
    else:
        while not((heading - 40) <= yawAngle <= (heading + 40)):
            drive_base.drive(0, -90)
            yawAngle = normalize_yaw(hub.imu.heading())
        while not((heading - 2) <= yawAngle <= (heading + 2)):
            drive_base.drive(0, -50)
            yawAngle = normalize_yaw(hub.imu.heading())
    drive_base.brake()

# (195, 733, 192, 866)
drive_base.settings(250, 650, 170, 800)
print("settings:", drive_base.settings())

print(path)
for i in range(len(path)-1):
    if (i%2) != 1:
        currentX, currentY = path[i]
        nextX, nextY = path[i+1]
        changeX = nextX-currentX # up down
        changeY = nextY-currentY # left right
        print(changeX, changeY)
        print("-----------")
        if changeX == -1:
            doubleTurn(2, "right")
            drive_base.straight(250)
            wait(500)
        elif changeX == 1:
            doubleTurn(2, "right")
            drive_base.straight(-250)
            wait(500)
        elif changeY == -1:
            doubleTurn(-88, "right")
            drive_base.straight(250)
            wait(500)
        elif changeY == 1:
            doubleTurn(92, "right")
            drive_base.straight(250)
            wait(500)
