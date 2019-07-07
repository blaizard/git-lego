#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

class Interface:
	def __init__(self):
		pass
	
	@staticmethod
	def getExtensions():
		return []

	def getCommandTagBegin(self):
		return ""

	def getCommandTagEnd(self):
		return ""

	def contentToLocal(self, content, namespace):
		return content

	def contentFromLocal(self, content, namespace):
		return content
