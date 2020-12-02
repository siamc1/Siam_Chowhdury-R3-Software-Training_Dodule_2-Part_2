import pygame
import time
import random
import math
import random
import socket

WIDTH = 800
HEIGHT = 800
FPS = 30
grid = []
visited = []
solVisited = []
availableSpaces = {}
solution = []

direction = {
    "N":[0,-1],
    "S":[0,1],
    "E":[1,0],
    "W":[-1,0],
}

n = 10
w = WIDTH/n
h = HEIGHT/n

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
white = [255, 255, 255]
black = [0,0,0]
screen.fill(white)
pygame.display.update()

def drawGrid(n):
    w = WIDTH/n
    h = HEIGHT/n
    x = 0.0
    y = 0.0
    for i in range(0,n):
        for j in range(0,n):
            pygame.draw.line(screen, black,[x,y],[x+w,y],2) # TOP
            pygame.draw.line(screen, black,[x, y], [x, y+h],2) # LEFT
            pygame.draw.line(screen, black,[x + w, y], [x + w, y + h],2) # RIGHT
            pygame.draw.line(screen, black,[x, y + h], [x+w, y + h],2) # BOTTOM
            grid.append([x,y])
            availableSpaces[(x,y)] = []
            x += w
        x = 0.0
        y += h
    print(len(grid))
    pygame.display.update()

def carveMazefrom(x,y,grid):
    if [x,y] in visited or [x,y] not in grid:
        return
    else:
        visited.append([x,y])


    dir_order = ["N","S","E","W"]
    random.shuffle(dir_order)

    for i in range(0,len(dir_order)):
        next_x = x + (direction.get(dir_order[i])[0])*w
        next_y = y + (direction.get(dir_order[i])[1])*h
        
        if [next_x, next_y] not in visited and [next_x, next_y] in grid:
            if dir_order[i] == "N":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["N"]
                pygame.draw.line(screen, white,[x,y],[x+w,y],2)
            if dir_order[i] == "S":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["S"]
                pygame.draw.line(screen, white,[x, y + h], [x+w, y + h],2) 
            if dir_order[i] == "E":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["E"]
                pygame.draw.line(screen, white,[x + w, y], [x + w, y + h],2) 
            if dir_order[i] == "W":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["W"]
                pygame.draw.line(screen, white,[x, y], [x, y+h],2)
            pygame.display.update()
            time.sleep(0.05) # Comment This If You Dont Want To Wait For Maze To Generate
            carveMazefrom(next_x,next_y,grid)
        
        



def solveMaze (x,y,aSpaces,grid,currentPath):
    if ((x,y) in currentPath):
        return
    currentPath.append((x,y))

    if (x,y) == (WIDTH-w,HEIGHT-h):
        solution[:] = list(currentPath)
        currentPath.pop()
        return

    for i in range(0,len(aSpaces.get((x,y)))):
        next_x = x + (direction.get(aSpaces.get((x,y))[i])[0])*w
        next_y = y + (direction.get(aSpaces.get((x,y))[i])[1])*h
        if aSpaces.get((x,y))[i] == "N":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "S":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "E":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "W":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
    currentPath.pop()
    return

            
drawGrid(n)
carveMazefrom(0,0,grid)
solveMaze(0,0,availableSpaces,grid,[])
for i in solution:
    pygame.draw.circle(screen, [255,0,0],[ i[0]+(w/2) , i[1]+(h/2)],10)
    pygame.display.update()
    time.sleep(0.05) # Comment This If You Dont Want To Wait For Solution To Generate

# Write your code here or make a new python file and run the code from here
# The array that contains the solution is called solution[], use this for the TCP Stream.

# Get's the host name and saves it to a varible
HOST = socket.gethostname()
# Defines which port the communications will be transferred through, Must be greater than 1023
PORT = 2020

# Creates a socket instance to handle communications over the netwerk
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binds the socket to the hostname and port
s.bind((HOST, PORT))

# sets the socket to listen for communication partners
s.listen()

# saves the details of the first partner found in two variables for future reference and prints a line saying that it was able to establish a connection
conn, addr = s.accept()
print('Conection from ' + str(addr) + ' has been established')

# creates a list to hold all moves which need to be transmitted as well as a variable which keeps track of the rovers direction
moves = []
direc = 'R'
# runs through all the positions the robot needs to travel to in the solution list and adds the appropriate messages to the moves list
for i in range(1, len(solution)):
	# variables to keep track of the position before and after the next move is made
	prevX, prevY = solution[i - 1]
	aftX, aftY = solution[i]
	# checks which direction the rover is displaced after the move to send the correct instructions
	if aftX > prevX:
		# checks which direction the rover is currently facing, and based on where it needs to go, it will send instructions to turn to the correctdirection and move forward one block
		if direc == 'R':
			# moves forward
			moves.append("[0][255][0][255]")
		elif direc == 'D':
			# turns left then moves forward
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'L':
			# turns 180 degrees by turning left twice before moving one block forward
			moves.append("[255][0][0][255]")
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'U':
			# turns right once before moving one block forward
			moves.append("[0][255][255][0]")
			moves.append("[0][255][0][255]")
		# sets the direction of the rover to the current direction it's facing after the move
		direc = 'R'

	elif aftX < prevX:
		if direc == 'L':
			moves.append("[0][255][0][255]")
		elif direc == 'U':
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'R':
			moves.append("[255][0][0][255]")
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'D':
			moves.append("[0][255][255][0]")
			moves.append("[0][255][0][255]")

		direc = 'L'

	elif aftY > prevY:
		if direc == 'D':
			moves.append("[0][255][0][255]")
		elif direc == 'L':
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'U':
			moves.append("[255][0][0][255]")
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'R':
			moves.append("[0][255][255][0]")
			moves.append("[0][255][0][255]")

		direc = 'D'

	elif aftY < prevY:
		if direc == 'U':
			moves.append("[0][255][0][255]")
		elif direc == 'R':
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'D':
			moves.append("[255][0][0][255]")
			moves.append("[255][0][0][255]")
			moves.append("[0][255][0][255]")
		elif direc == 'L':
			moves.append("[0][255][255][0]")
			moves.append("[0][255][0][255]")

		direc = 'U'

# appends the final instruction to stop all motors to the end of the moves list
moves.append("[0][0][0][0]")

# runs through and sends all the moves to the rover, with 1 second buffers inbetween each instruction
for i in range(len(moves)):
	# sends the instruction in the form of  bytes with utf-8 encoding
	conn.send(bytes(moves[i], "utf-8"))
	#pauses the program for 1 second
	time.sleep(1)



running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



