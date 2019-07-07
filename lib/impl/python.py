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
		codeVarName = "_gitlego%i" % (self.unique)
		content = "%s = \"\"\"%s\"\"\"\n" % (codeVarName, content.replace("\\", "\\\\").replace("\"\"\"", "\\\"\"\""))
		content += "import imp\n"
		if namespace not in self.namespaces:
			content += "%s = imp.new_module(\"%s\")\n" % (namespace, namespace)
			content += "%s.__dict__[\"__file__\"] = __file__\n" % (namespace)
		content += "exec(%s, %s.__dict__)" % (codeVarName, namespace)

		self.unique += 1
		self.namespaces.add(namespace)

		return content
