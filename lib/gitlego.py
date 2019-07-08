#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
import re
import shlex
import subprocess
import zlib

class GitLego:

	def __init__(self, filePath, cwd = None, implClass = None):

		self.impl = implClass()

		self.filePath = os.path.realpath(filePath)
		with open(self.filePath, "r") as file:
			self.content = file.read()

		# Set the current working directory
		self.cwd = os.path.join(os.path.join(os.path.dirname(self.filePath), ".git-lego") if cwd == None else os.path.realpath(cwd))

		# The matching pattern for a command
		self.commandPattern = re.compile(r"""
				^%s\s*git-lego\s+               # Match with the header
				\b(?P<command>\w+)\b            # The command
				\s*?\b(?P<args>.*?)$            # Optional arguments
				""" % (re.escape(self.impl.getCommandTagBegin())), re.VERBOSE | re.MULTILINE)

		# Command options
		self.commandOptionPattern = re.compile(r"""
				\[\s*(?P<key>[a-zA-Z]+)\s*=\s*(?P<value>[^\]]*)\s*\] # Match [key=value] type
				""", re.VERBOSE)

		# Definition data for parsing
		self.definition = {
			"dep": {
				"command": True,
				"block": "maybe",
				"args": [
					{"name": "remote", "regexpr": "(https?://|ssh://|file://).+", "required": True},
					{"name": "local", "regexpr": ".+", "required": True},
					{"name": "branch", "regexpr": ".+", "required": False, "default": "master"},
					{"name": "namespace", "regexpr": "[a-zA-Z0-9_]+", "required": False, "default": "gitlego"},
					{"name": "checksum", "regexpr": "[0-9]+", "required": False, "default": 0},
				]
			},
			"end": {
				"command": False,
				"block": "no"
			},
		}

		self.data = []

	"""
	Get the line number in the content form the index
	"""
	def getLineNumber(self, index):
		pos = -1
		nbLines = 0
		while pos < index:
			pos = self.content.find("\n", pos + 1)
			if pos == -1:
				break
			nbLines += 1
		return nbLines

	def shell(self, command, cwd = None):
		if subprocess.call(command, cwd=cwd) != 0:
			self.logFatal("Error while running shell command: %s" % (str(command)))

	"""
	Translate a path into a hash
	"""
	def generateLocalDependencyPath(self, remote, local = ""):
		return os.path.join(self.cwd, re.sub(r"[^\w]+", ".", remote), local)

	def checksum(self, data):
		return zlib.crc32(data.strip().encode("utf-8")) & 0xffffffff

	def logFatal(self, message, index = -1):
		pre = ("Error at line %i: " % (self.getLineNumber(index))) if index >= 0 else ""
		print("[fatal] %s%s" % (pre, message))
		sys.exit(2)

	"""
	Parse the file and build the data structure
	"""
	def parse(self):

		data = []
		self.data = []

		# Analyze the tags in the file
		for match in self.commandPattern.finditer(self.content):

			command = match.group("command").strip()
			args = match.group("args").strip()
			line = self.getLineNumber(match.start())

			if command in self.definition:
				# Save the data
				data.append({
					"start": match.start(),
					"end": match.end(),
					"command": command,
					"args": args
				})
			else:
				self.logFatal("Unknown command '%s'" % (command), match.start())

		# Group command with their respective block (if any) together
		i = 0
		while i < len(data):
			item = data[i]
			nextItem = data[i + 1] if (i + 1 < len(data)) else None
			i += 1
			definition = self.definition[item["command"]]

			# If the next command is a block
			isNextBlock = True if nextItem and (nextItem["command"] == "end") else False
			if isNextBlock:
				if definition["block"] == "no":
					self.logFatal("Command '%s' do not accept blocks" % (item["command"]), item["start"])
				item.update({
					"blockStart": item["end"],
					"blockEnd": nextItem["start"],
					"end": nextItem["end"]
				})
				i += 1
			elif definition["block"] == "yes":
				self.logFatal("Command '%s' must be a block" % (item["command"]), item["start"])

			# Sanity check, ensure that only valid commands are parsed
			if not definition["command"]:
				self.logFatal("The command '%s' is used incorrectly" % (item["command"]), item["start"])

			# Decode arguments
			definitionDict = { argDef["name"] : argDef for i, argDef in enumerate(definition["args"]) }
			argList = shlex.split(item["args"])
			parseOption = False
			for index, argDef in enumerate(definition["args"]):

				# Current definition
				curDef = argDef

				# An argument is available
				if index < len(argList):
					arg = argList[index]

					# Check if this is an option
					matchOption = re.match(self.commandOptionPattern, arg)
					if matchOption:
						parseOption = True
						# Look for the matching option
						key = matchOption.group("key").strip()
						if key in definitionDict:
							curDef = definitionDict[key]
							arg = matchOption.group("value").strip()
						else:
							self.logFatal("Unknow option key '%s' from command '%s'" % (key, item["command"]), item["start"])
					elif parseOption:
						self.logFatal("Arguments cannot follow options in command '%s'" % (item["command"]), item["start"])

					if re.match(curDef["regexpr"], arg):
						item[curDef["name"]] = arg
					else:
						self.logFatal("Argument '%s' of command '%s' should match: %s" % (arg, item["command"], curDef["regexpr"]), item["start"])
				elif curDef["required"] == False:
					item[curDef["name"]] = curDef["default"]
				else:
					self.logFatal("Command '%s' requires at least %i arguments" % (item["command"], index + 1), item["start"])

			# Save the data
			self.data.append(item)

		#print(self.data)

	"""
	Fetch the dependencies
	"""
	def fetch(self):
		if not os.path.isdir(self.cwd):
			os.mkdir(self.cwd)

		# First fetch all dependencies
		for remote in set(item["remote"] for item in self.data if item["command"] == "dep"):
			path = self.generateLocalDependencyPath(remote)
			if not os.path.isdir(path):
				os.mkdir(path)
				self.shell(["git", "clone", remote, path])
			else:
				self.shell(["git", "pull"], cwd=path)

	"""
	Update dependencies
	"""
	def update(self):

		contentUpdated = ""
		index = 0

		for dep in [item for item in self.data if item["command"] == "dep"]:
			localPath = self.generateLocalDependencyPath(dep["remote"], dep["local"])
			if not os.path.isfile(localPath):
				self.logFatal("The file '%s' referred by the 'dep' command does not exists locally" % (localPath), dep["start"])

			# Start the copy the original file
			contentUpdated += self.content[index:dep["start"]]
			index = dep["end"]

			# Copy the content of the local dependency
			localContent = ""
			with open(localPath, "r") as localHandle:
				localContent = localHandle.read()

			localContent = self.impl.contentToLocal(localContent, dep["namespace"])

			contentUpdated += "%s git-lego dep \"%s\" \"%s\" \"[branch=%s]\" \"[namespace=%s]\" [checksum=%i]%s\n" % (self.impl.getCommandTagBegin(), dep["remote"], dep["local"], dep["branch"], dep["namespace"], self.checksum(localContent), self.impl.getCommandTagEnd())
			contentUpdated += localContent
			contentUpdated += "\n%s git-lego end%s\n" % (self.impl.getCommandTagBegin(), self.impl.getCommandTagEnd())

		# Copy the rest of the original file
		contentUpdated += self.content[index:]

		# Replace the orginal file content (note do not move the file as we want to keep permissions and owner)
		with open(self.filePath, "w") as fileHandle:
			fileHandle.write(contentUpdated)

	"""
	Give the status of the git entries
	"""
	def status(self):

		status = {
			"modified": [],
			"missing": []
		}

		# Read the content of each dependencies and check the checksum 
		for dep in [item for item in self.data if item["command"] == "dep"]:

			# If this is a block
			if "blockStart" in dep and "blockEnd" in dep:
				content = self.content[dep["blockStart"]:dep["blockEnd"]]
				checksum = self.checksum(content)
				if checksum != int(dep["checksum"]):
					status["modified"].append({
						"content": content,
						"dep": dep
					})
			else:
				status["missing"].append({
					"dep": dep
				})

		return status
