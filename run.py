#!/usr/bin/env python2
import server
import client
import controller
import fallback
import random
import time
import thread

# Run in a separate thread. Updates the board @ 10Hz.
def run_controller(gamecontroller, m_game):
	while(True):
		m_game = gamecontroller.calc_grid(m_game)
		gamecontroller.set_game_matrix(m_game)
		time.sleep(0.1)

def main():
	# Initialize a game controller (every device needs one in case it becomes the server).
	gamecontroller = controller.Controller()
	# Initial state doesn't exist until first server is selected.
	current_state = None
	

	device = fallback.Device('./iplist.conf', gamecontroller)


	while(True):
		# To minimize the possibility of more than one device becoming the server when it goes down.
		time.sleep(random.random())

		if (device.identify_server() == 0):

			device.become_server()

			# To maintain board state between servers when falling back.
			if current_state:
				game = current_state

			# Initialize the board state the first time only.
			else:
				game = gamecontroller.init_mat()

			# Start updating the board @ 10Hz. (Threaded because it's blocking.)
			thread.start_new_thread(run_controller, (gamecontroller, game))

			while(True):
				device.serve()

		else:
			# Device's remote_server is set when it finds a server while searching above.
			myclient = client.Client(device.get_remote_server())
			server_online = True

			while(server_online):
				try:
					myclient.connect()
					# Get the updated board from the server.
					myclient.send("update")
					myclient.recv()
					myclient.process()
					# Update the current board state in case this device becomes the new server.
					current_state = myclient.get_state()
				except:
					server_online = False
					break
				myclient.close()
				# Do this loop @ 10Hz.
				time.sleep(0.1)

if __name__ == '__main__':
	main()

