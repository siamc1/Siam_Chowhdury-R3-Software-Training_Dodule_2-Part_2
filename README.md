# Siam_Chowhdury-R3-Software-Training_Dodule_2-Part_2
In this module, the task was to transmit readable instructions to the motor controller in order to allow the rover to traverse the solution to any given maze.

To do this, I assumed the following:
  Each movement will take 1 second to complete
  When the rover recieved the appropriate instruction for right or left, it would turn right 90 degrees in 1 second
  There will only be the rover trying to connect to the controller over this specific port (2020)

When solving this module, I decided to first assemble a list containing all the moves needed to be transmitted to the rover, and then transmitting them after.
This method is slower than the method in which you would transfer instructions right after they are computed, however this is more reliable, as if there are any issues with the translation of soltuion to instructions, it's impossible to know until after the rover has already started moving.

My code requires the user to specify which direction the rover is facing in the maze, with the starting position being the top left square and the end at the bottom right

For my reciever code, it will connect to the first master device looking for connections through the port 2020

The transmission happens by running through all the instructions that need to be transmitted, converting them to bytes using utf-8 and transmitting them over TCP

it will then constantly look for messages, and when one is found, it will print it to the console
