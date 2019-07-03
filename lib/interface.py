#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from . import gitlego

class Interface():

	def __init__(self, filePath, cwd = None):
		self.gitLego = gitlego.GitLego(filePath, cwd=cwd)

	def update(self, force = False):

		self.gitLego.parse()
		self.gitLego.fetch()
		status = self.gitLego.status()

		# Check if there is anything to update
		if force or len(status["modified"]) == 0:
			self.gitLego.update()
		else:
			print("Please commit modified files first:")
			for modified in status["modified"]:
				dep = modified["dep"]
				print("\tmodified: %s %s %s (line: %i..%i)" % (dep["remote"], dep["local"], dep["branch"], self.gitLego.getLineNumber(dep["start"]), self.gitLego.getLineNumber(dep["end"])))

	def status(self):

		self.gitLego.parse()
		status = self.gitLego.status()

		uptodate = True

		for modified in status["modified"]:
			dep = modified["dep"]
			print("\tmodified: %s %s %s (line: %i..%i)" % (dep["remote"], dep["local"], dep["branch"], self.gitLego.getLineNumber(dep["start"]), self.gitLego.getLineNumber(dep["end"])))
			uptodate = False

		for missing in status["missing"]:
			dep = missing["dep"]
			print("\tmissing: %s %s %s (line: %i)" % (dep["remote"], dep["local"], dep["branch"], gitLego.getLineNumber(dep["start"])))
			uptodate = False

		if uptodate:
			print("Already up to date.")
