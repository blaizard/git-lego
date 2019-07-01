#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import argparse
import os
import re
import shlex
import subprocess

## git-lego dep https://github.com/blaizard/irapp.git /.irapp/lib.py


#This is a test

## git-lego end

## git-lego dep https://github.com/blaizard/irapp.git dsf


class GitLego:

	def __init__(self, fileName, cwd = None):

		with open(fileName, "r") as file:
			self.content = file.read()

		# Set the current working directory
		self.cwd = os.path.join(os.path.dirname(os.path.abspath(fileName)) if cwd == None else os.path.abspath(cwd), ".git-lego")

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
					{"name": "remote", "regexpr": "(https?://|ssh://|file://).*", "required": True},
					{"name": "local", "regexpr": ".*", "required": True},
					{"name": "tag", "regexpr": ".*", "required": False, "default": None},
					{"name": "checksum", "regexpr": ".*", "required": False, "default": None},
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
	def pathToHash(self, path):
		return re.sub(r"[^\w]+", ".", path)

	def logFatal(self, message, line = None):
		pre = ("Error at line %i: " % (line)) if line else ""
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
					"start": line,
					"end": line,
					"command": command,
					"args": args
				})
			else:
				self.logFatal("Unknown command '%s'" % (command), line)

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
					item[argDef["name"]] = None
				else:
					self.logFatal("Command '%s' requires at least %i arguments" % (item["command"], index + 1), item["start"])

			# Save the data
			self.data.append(item)

		#print(self.data)

	"""
	Process the previously parsed file
	"""
	def process(self):
		if not os.path.isdir(self.cwd):
			os.mkdir(self.cwd)

		# First fetch all dependencies
		for remote in set(item["remote"] for item in self.data if item["command"] == "dep"):
			pathHash = self.pathToHash(remote)
			path = os.path.join(self.cwd, pathHash)
			if not os.path.isdir(path):
				os.mkdir(path)
				self.shell(["git", "clone", remote, path])
			else:
				self.shell(["git", "pull"], cwd=path)

		# Update the files

def gitLegoUpdate():

	gitLego = GitLego(os.path.abspath(__file__))
	gitLego.parse()
	gitLego.process()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = "Git lego project manager.")
	subparsers = parser.add_subparsers(dest="command", help="Available commands.")
	parserRun = subparsers.add_parser("update", help="Update the current dependencies to their last version.")
	args = parser.parse_args()

	# Excecute the action
	if args.command == "update":
		gitLegoUpdate()

	sys.exit(0)
