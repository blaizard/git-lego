#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from . import interface

class TypePython(interface.Interface):

	def getCommandTagBegin(self):
		return "##"

	def getCommandTagEnd(self):
		return ""

	def contentToLocal(self, content, namespace):

		# Format the localContent to use a namespace for the piece of code
		content = "\"\"\"%s\"\"\"" % (content.replace("\\", "\\\\").replace("\"\"\"", "\\\"\"\""))
		updatedContent = "import imp\n"
		updatedContent += "%s = imp.new_module(\"%s\") if \"%s\" not in locals() else %s\n" % (namespace, namespace, namespace, namespace)
		updatedContent += "%s.__dict__[\"__file__\"] = __file__\n" % (namespace)
		updatedContent += "exec(%s, %s.__dict__)" % (content, namespace)

		return updatedContent
