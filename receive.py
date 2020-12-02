import socket

# creates variables for the host name and the communication port. Note that the port must be the same for both reciever and sender
HOST = socket.gethostname()
PORT = 2020

# creates a new instance of socket to communicate over the network and connects it to the specified port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# will run until instructions stop arriving
isRunning = True
while isRunning:
	# recieves an instruction and saves it to a variable before decoding the instruction and overwriting the previous encoded value to the decoded vale
	comm = s.recv(1024)
	comm = comm.decode("utf-8")
	# checks to see if the length of the instruction is less than or equal to 0, and if so, will stop looping
	if len(comm) <= 0:
		isRunning = False
	# prints the instruction to the console
	print(comm)