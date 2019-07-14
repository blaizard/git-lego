#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import argparse
import os

from . import gitlego
from . import impl

class Interface():

	def __init__(self, filePath, cwd = None, type = None):

		ext = filePath.split(".")[-1].lower()
		implClass = impl.definitions[ext] if ext in impl.definitions else types.interface

		self.fileName = os.path.basename(filePath)
		self.gitLego = gitlego.GitLego(filePath, cwd=cwd, implClass=implClass)

	def run(self, command):

		parser = argparse.ArgumentParser(description = "git-lego is a script dependency manager")
		subparsers = parser.add_subparsers(dest="command", help="Available commands")
		parserUpdate = subparsers.add_parser("update", help="Update the current dependencies to their lastest version")
		parserUpdate.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Force the update, disregarding local modifications")
		subparsers.add_parser("status", help="Show the status of the current file")
		args = parser.parse_args(command)

		# Excecute the action
		if args.command == "update":
			self.update(args.force)
		elif args.command == "status":
			self.status()

		return 0

	def update(self, force = False):

		self.gitLego.parse()
		self.gitLego.fetch()
		status = self.gitLego.status()

		# Check if there is anything to update
		if force or len(status["modified"]) == 0:
			self.gitLego.update()

		else:
			print("%s is not in a consistent state." % (self.fileName))
			print("(use the '--force' option to discard local changes)")
			self._status(status, onlyModified=True, onlyContent=True)

	def status(self, onlyModified=False, onlyContent=False):

		self.gitLego.parse()
		status = self.gitLego.status()
		self._status(status, onlyModified=False, onlyContent=False)

	def _status(self, status, onlyModified=False, onlyContent=False):

		uptodate = len(status["modified"]) == 0 and len(status["missing"]) == 0

		if uptodate:
			if not onlyContent:
				print("%s is in a consistent state." % (self.fileName))
				print("(use the 'update' command to fetch the latest updates from remote)")

		else:
			if not onlyContent:
				print("%s is not in a consistent state." % (self.fileName))
				print("(use the 'update' command to fetch the latest updates from remote)")

			if len(status["modified"]):
				uptodate = False
				print("\nModified entries:\n")
				for modified in status["modified"]:
					dep = modified["dep"]
					print("\t%s %s %s (line: %i..%i)" % (dep["remote"], dep["local"], dep["branch"], self.gitLego.getLineNumber(dep["start"]), self.gitLego.getLineNumber(dep["end"])))
				print("")

			if len(status["missing"]) and onlyModified == False:
				uptodate = False
				print("Missing entries:\n")
				for missing in status["missing"]:
					dep = missing["dep"]
					print("\t%s %s %s (line: %i)" % (dep["remote"], dep["local"], dep["branch"], gitLego.getLineNumber(dep["start"])))
				print("")
