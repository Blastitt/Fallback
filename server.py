#!/usr/bin/env python2

import socket

class Server():

	def __init__(self, host, port):

		self.host = host
		self.port = port
		self.connection = None

		self.client = None
		self.clientaddr = None

		self.data = None

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
		#try:
		self.client, self.clientaddr = self.connection.accept()
		print("[+] Connection received from " + str(self.clientaddr))
		self.data = self.client.recv(2048)
		print(self.data)
		#except Exception as e:
			#print("[!] Error receiving from client: " + str(e))

	def process(self):

		if(self.data.strip("\r\n") == "heartbeat"):
			msg = "heartbeat received"
			print("[+] Sending message...")
			self.client.sendall(msg)
			self.client.close()


def main():
	server = Server('0.0.0.0', 8000)

	server.start()

	while(True):

		server.recv()
		server.process()

if __name__ == '__main__':
	main()