#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from . import interface

class TypePython(interface.Interface):
	def __init__(self):
		self.unique = 0
		self.namespaces = set()

	def getCommandTagBegin(self):
		return "##"

	def getCommandTagEnd(self):
		return ""

	def contentToLocal(self, content, namespace):

		# Format the localContent to use a namespace for the piece of code
		content = "\"\"\"%s\"\"\"" % (content.replace("\\", "\\\\").replace("\"\"\"", "\\\"\"\""))
		updatedContent = "import imp\n"
		if namespace not in self.namespaces:
			updatedContent += "%s = imp.new_module(\"%s\")\n" % (namespace, namespace)
			updatedContent += "%s.__dict__[\"__file__\"] = __file__\n" % (namespace)
		updatedContent += "exec(%s, %s.__dict__)" % (content, namespace)

		self.unique += 1
		self.namespaces.add(namespace)

		return updatedContent
