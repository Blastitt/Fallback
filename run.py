#!/usr/bin/env python2
import server
import client
import controller
import fallback
import random
import time

def main():
	device = fallback.Device('./iplist.conf')

	while(True):
		time.sleep(random.random())
		if (  device.identify_server() == 0):

			device.become_server()

			while(True):
				device.serve()

		else:
			client = client.Client(device.get_remote_server())
			server_online = True

			while(server_online):
				try:
					client.connect()
					client.send("heartbeat")
					client.recv()
				except:
					server_online = false
					break
				data = client.getdata()
				if(data):
					print(data)
				client.close()
				time.sleep(0.1)

if __name__ == '__main__':
	main()

