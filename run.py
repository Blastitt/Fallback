#!/usr/bin/env python2
import server
import client
import controller
import fallback
import random
import time
import thread

def run_controller(gamecontroller, m_game):
	while(True):
		m_game = gamecontroller.calc_grid(m_game)
		gamecontroller.set_game_matrix(m_game)
		time.sleep(0.1)

def main():
	gamecontroller = controller.Controller()
	game = gamecontroller.init_mat()

	device = fallback.Device('./iplist.conf', gamecontroller)

	thread.start_new_thread(run_controller, (gamecontroller, game))

	while(True):
		time.sleep(random.random())
		if (  device.identify_server() == 0):

			device.become_server()

			while(True):
				device.serve()

		else:
			myclient = client.Client(device.get_remote_server())
			server_online = True

			while(server_online):
				try:
					myclient.connect()
					myclient.send("heartbeat")
					myclient.recv()
				except:
					server_online = False
					break
				data = myclient.getdata()
				if(data):
					print(data)
				myclient.close()
				time.sleep(0.1)

if __name__ == '__main__':
	main()

