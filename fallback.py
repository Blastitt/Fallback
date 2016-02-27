#!/usr/bin/env python2

import server
import client
import controller

class Device():

	def __init__(self, ipfile):

		self.ipfile = open(ipfile, 'r')
		self.iplist = []

		self.is_server= False

		self.remote_server = None


		self.server = None

	def parse_ips(self):
		print("[+] Parsing IP File...")
		for line in self.ipfile:
			self.iplist.append(line.strip("\r\n"))

	def identify_server(self):
		self.parse_ips()

		for ip in self.iplist:
			host = ip.split(':')[0]
			port = int(ip.split(':')[1])

			myclient = client.Client((host, port))

			try:
				if myclient.connect():
					self.remote_server = (host, port)
					return 1
			except:
				continue

		return 0


	def become_server(self):

		print("[!] No server found - Becoming Server!")

		self.server = server.Server('', 8000)
		self.is_server = True

		self.server.start()

	def serve(self):
		if self.is_server:
			self.server.recv()
			self.server.process()

	def get_remote_server(self):

		return self.remote_server

	def is_server(self):

		return self.is_server