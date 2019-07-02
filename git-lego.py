#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import argparse
import os
import re
import shlex
import subprocess
import zlib

## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" 2882168141
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

class Commands:

	@staticmethod
	def cd(context, argList):
		if len(argList) != 1:
			raise Exception("Malformed cd command, must take exactly 1 argument.")
		newPath = os.path.join(context["cwd"], argList[0])
		newPath = os.path.normpath(newPath)
		if not os.path.isdir(newPath):
			raise Exception("Directory '%s' does not exists." % (newPath))
		context["cwd"] = newPath

	@staticmethod
	def sleep(context, argList):
		if len(argList) != 1:
			raise Exception("Malformed sleep command, must take exactly 1 argument.")
		time.sleep(float(argList[0]))

## git-lego end


# Tell me more!

## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" 2882168141
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

class Commands:

	@staticmethod
	def cd(context, argList):
		if len(argList) != 1:
			raise Exception("Malformed cd command, must take exactly 1 argument.")
		newPath = os.path.join(context["cwd"], argList[0])
		newPath = os.path.normpath(newPath)
		if not os.path.isdir(newPath):
			raise Exception("Directory '%s' does not exists." % (newPath))
		context["cwd"] = newPath

	@staticmethod
	def sleep(context, argList):
		if len(argList) != 1:
			raise Exception("Malformed sleep command, must take exactly 1 argument.")
		time.sleep(float(argList[0]))

## git-lego end












class GitLego:

	def __init__(self, filePath, cwd = None):

		self.filePath = os.path.abspath(filePath)
		with open(self.filePath, "r") as file:
			self.content = file.read()

		# Set the current working directory
		self.cwd = os.path.join(os.path.dirname(self.filePath) if cwd == None else os.path.abspath(cwd), ".git-lego")
		self.deps = os.path.join(self.cwd, "deps")

		# The matching pattern for a command
		self.commandPattern = re.compile(r"""
				^\#\#\s*git-lego\s+               # Match with the header
				\b(?P<command>\w+)\b              # The command
				\s*?\b(?P<args>.*?)$              # Optional arguments
				""", re.VERBOSE | re.MULTILINE)

		# Definition data for parsing
		self.definition = {
			"dep": {
				"command": True,
				"block": "maybe",
				"args": [
					{"name": "remote", "regexpr": "(https?://|ssh://|file://).+", "required": True},
					{"name": "local", "regexpr": ".+", "required": True},
					{"name": "branch", "regexpr": ".+", "required": False, "default": "master"},
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
		return os.path.join(self.deps, re.sub(r"[^\w]+", ".", remote), local)

	def checksum(self, data):
		return zlib.crc32(data.strip()) & 0xffffffff

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

			if self.definition.has_key(command):
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
			argList = shlex.split(item["args"])
			for index, argDef in enumerate(definition["args"]):
				# An argument is available
				if index < len(argList):
					arg = argList[index]
					if re.match(argDef["regexpr"], arg):
						item[argDef["name"]] = arg
					else:
						self.logFatal("Argument '%s' of command '%s' should match: %s" % (arg, item["command"], argDef["regexpr"]), item["start"])
				elif argDef["required"] == False:
					item[argDef["name"]] = argDef["default"]
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
			if not os.path.isdir(self.deps):
				os.mkdir(self.deps)

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
				self.logFatal("The file '%s' referred by the 'dep' command does not exists locally" % (localPath), item["start"])

			# Start the copy the original file
			contentUpdated += self.content[index:dep["start"]]
			index = dep["end"]

			# Copy the content of the local dependency
			localContent = ""
			with open(localPath, "r") as localHandle:
				localContent = localHandle.read()
			contentUpdated += "## git-lego dep \"%s\" \"%s\" \"%s\" %i\n" % (dep["remote"], dep["local"], dep["branch"], self.checksum(localContent))
			contentUpdated += localContent
			contentUpdated += "\n## git-lego end\n"

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
			"newer": []
		}

		# Read the content of each dependencies and check the checksum 
		for dep in [item for item in self.data if item["command"] == "dep"]:

			content = ""

			# If this is a block
			if dep.has_key("blockStart") and dep.has_key("blockEnd"):
				content = self.content[dep["blockStart"]:dep["blockEnd"]]
				checksum = self.checksum(content)
				if checksum != int(dep["checksum"]):
					status["modified"].append({
						"content": content,
						"dep": dep
					})

			# Check if there is an updated version upstream
			localPath = self.generateLocalDependencyPath(dep["remote"], dep["local"])
			if os.path.isfile(localPath):
				with open(localPath, "r") as localHandle:
					localContent = localHandle.read()
					localChecksum = self.checksum(localContent)

					# Means that a newer version has been fetched
					if localChecksum != int(dep["checksum"]):
						status["newer"].append({
							"localContent": localContent,
							"content": content,
							"dep": dep
						})

		return status

def gitLegoUpdate():

	gitLego = GitLego(os.path.abspath(__file__))
	gitLego.parse()
	gitLego.fetch()
	status = gitLego.status()

	# Check if there is anything to update
	if len(status["newer"]):
		gitLego.update()

def gitLegoStatus():

	gitLego = GitLego(os.path.abspath(__file__))
	gitLego.parse()
	status = gitLego.status()

	uptodate = True

	if len(status["modified"]):
		for modified in status["modified"]:
			dep = modified["dep"]
			print("\tmodified: %s %s %s" % (dep["remote"], dep["local"], dep["branch"]))
			uptodate = False

	if len(status["newer"]):
		for newer in status["newer"]:
			dep = newer["dep"]
			print("\tnewer: %s %s %s" % (dep["remote"], dep["local"], dep["branch"]))
			uptodate = False

	if uptodate:
		print("Already up to date.")

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = "Git lego project manager.")
	subparsers = parser.add_subparsers(dest="command", help="Available commands.")
	subparsers.add_parser("update", help="Update the current dependencies to their last version.")
	subparsers.add_parser("status", help="Gives the status of the current file.")
	args = parser.parse_args()

	# Excecute the action
	if args.command == "update":
		gitLegoUpdate()
	elif args.command == "status":
		gitLegoStatus()

	sys.exit(0)
