#!/usr/bin/env python2

import socket

class Client():

	def __init__(self, serverhost, serverport):

		self.serverhost = serverhost
		self.serverport = serverport
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.data = None

	def connect(self):
		try:
			self.connection.connect((self.serverhost, self.serverport))
		except Exception as e:
			print("[!] Error connecting to server: " + str(e))

	def send(self, message):
		try:
			self.connection.sendall(message)
		except Exception as e:
			print("[!] Error sending to server: " + str(e))

	def recv(self):
		try:
			self.data = self.connection.recv(2048)
		except Exception as e:
			print("[!] Error receiving data from server: " + str(e))

	def getdata(self):

		return self.data

	def close(self):
		self.connection.close()
		return 0

def main():

	client = Client('0.0.0.0', 8000)

	client.connect()
	client.send("heartbeat")
	client.recv()
	data = client.getdata()
	if(data):
		print(data)
	client.close()

if __name__ == '__main__':
	main()