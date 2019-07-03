#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import argparse
import os
import re
import shlex
import subprocess
import zlib

## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "master"
import os
import subprocess
import sys
import imp
def gitLegoLoader(command = None):
	if len(sys.argv) < 2 or sys.argv[1] != "git-lego": return
	gitLegoPath = os.path.join(os.path.realpath(os.path.expanduser("~") if os.path.expanduser("~") else os.path.dirname(__file__)), ".git-lego")
	if not os.path.isdir(gitLegoPath): os.mkdir(gitLegoPath)
	gitLegoDepPath = os.path.join(gitLegoPath, "https.github.com.blaizard.git-lego.git")
	if not os.path.isdir(gitLegoDepPath): subprocess.call(["git", "clone", "https://github.com/blaizard/git-lego.git", gitLegoDepPath])
	lib = imp.load_module("lib", None, os.path.join(gitLegoDepPath, "lib"), ('', '', imp.PKG_DIRECTORY))
	gitlego = lib.interface.Interface(__file__, cwd=gitLegoPath)
	sys.exit(gitlego.run(command) if command else gitlego.run(sys.argv[2:]))
## git-lego end

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





def gitLegoUpdate(force = False):

	gitLego = GitLego(os.path.realpath(__file__))
	gitLego.parse()
	gitLego.fetch()
	status = gitLego.status()

	# Check if there is anything to update
	if force or len(status["modified"]) == 0:
		gitLego.update()
	else:
		print("Please commit modified files first:")
		for modified in status["modified"]:
			dep = modified["dep"]
			print("\tmodified: %s %s %s (line: %i..%i)" % (dep["remote"], dep["local"], dep["branch"], gitLego.getLineNumber(dep["start"]), gitLego.getLineNumber(dep["end"])))


def gitLegoStatus():

	gitLego = GitLego(os.path.realpath(__file__))
	gitLego.parse()
	status = gitLego.status()

	uptodate = True

	for modified in status["modified"]:
		dep = modified["dep"]
		print("\tmodified: %s %s %s (line: %i..%i)" % (dep["remote"], dep["local"], dep["branch"], gitLego.getLineNumber(dep["start"]), gitLego.getLineNumber(dep["end"])))
		uptodate = False

	for missing in status["missing"]:
		dep = missing["dep"]
		print("\tmissing: %s %s %s (line: %i)" % (dep["remote"], dep["local"], dep["branch"], gitLego.getLineNumber(dep["start"])))
		uptodate = False

	if uptodate:
		print("Already up to date.")

if __name__ == "__main__":

	gitLegoLoader()

	sys.exit(0)
