#!/usr/bin/env python2

import socket
import controller
import threading
import visuals

class Server():

	def __init__(self, host, port, gamecontroller):

		self.host = host
		self.port = port
		self.connection = None

		self.client = None
		self.clientaddr = None

		self.data = None
		self.update_msg = None

		self.gamecontroller = gamecontroller
	
		self.lights = visuals.Lights()

		self.subsection = None

	def start(self):
		try:
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.connection.bind((self.host, self.port))
			self.connection.listen(5)


		except Exception as e:
			print("[!] Error starting server: " + str(e))

	def stop(self):
		self.connection.close()

	def recv(self):
		try:
			self.client, self.clientaddr = self.connection.accept()
			print("[+] Connection received from " + str(self.clientaddr))
			self.data = self.client.recv(2048)
		except Exception as e:
			print("[!] Error receiving from client: " + str(e))

	def process(self):

		if(self.data.strip("\r\n") == "update"):
			self.update_msg = self.gamecontroller.get_game_data()
			print("[+] Sending game data...")
			print("[+] Current grid position: ", self.gamecontroller.get_grid_position())
			self.client.sendall(self.update_msg)
			self.client.close()
			self.update_lights()

	def update_lights(self):
		self.lights.update(self.gamecontroller.get_partial_grid())


def main():
	server = Server('', 8000)

	server.start()

	while(True):

		server.recv()
		server.process()

if __name__ == '__main__':
	main()
