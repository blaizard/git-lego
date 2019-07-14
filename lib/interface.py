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
		parserCommit = subparsers.add_parser("commit", help="Record changes to the repository")
		parserCommit.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Force the commit, disregarding differences with the source")
		parserCommit.add_argument("-m", "--message", required=True, dest="message", help="Use the given text as the commit message.")
		args = parser.parse_args(command)

		# Excecute the action
		if args.command == "update":
			self.update(args.force)
		elif args.command == "status":
			self.status()
		elif args.command == "commit":
			self.commit(args.force, args.message)

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
			self._status(status, includeList=["modified"], onlyContent=True)

	def status(self):

		self.gitLego.parse()
		status = self.gitLego.status()
		self._status(status)

	def commit(self, force=False, message=""):

		self.gitLego.parse()
		self.gitLego.fetch()
		status = self.gitLego.status()

		if len(status["modified"]) == 0:
			print("There is nothing to commit.")

		elif force == False and len(status["unsync"]) > 0:
			print("%s is not in-sync." % (self.fileName))
			print("(use the '--force' option to discard remote changes)")
			self._status(status, includeList=["unsync"], onlyContent=True)

		else:
			self.gitLego.commit(message)
			self.gitLego.update()


	def _status(self, status, includeList=["modified", "missing", "unsync"], onlyContent=False):

		definitions = {
			"modified": {
				"text": "Modified entries:",
				"singleLine": False
			},
			"missing": {
				"text": "Missing entries:",
				"singleLine": True
			},
			"unsync": {
				"text": "Entries are not in-sync:",
				"singleLine": False
			}
		}

		if len([1 for name in includeList if len(status[name]) != 0]) == 0:
			if not onlyContent:
				print("%s is in a consistent state." % (self.fileName))
				print("(use the 'update' command to fetch the latest updates from remote)")

		else:
			if not onlyContent:
				print("%s is not in a consistent state." % (self.fileName))
				print("(use the 'update' command to fetch the latest updates from remote)")

			for name in includeList:

				if len(status[name]):
					definition = definitions[name]
					print("\n%s\n" % (definition["text"]))
					for item in status[name]:
						dep = item["dep"]
						lineNumberStr = ("%i" % (self.gitLego.getLineNumber(dep["start"]))) if definition["singleLine"] else ("%i..%i" % (self.gitLego.getLineNumber(dep["start"]), self.gitLego.getLineNumber(dep["end"])))
						print("\t%s %s %s (line: %s)" % (dep["remote"], dep["local"], dep["branch"], lineNumberStr))
					print("")
