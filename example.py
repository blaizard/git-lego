#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import imp
def gitLegoLoader(command = None):
	import lib
	gitlego = lib.interface.Interface(__file__, cwd=".")
	sys.exit(gitlego.run(command) if command else gitlego.run(sys.argv[2:]))

## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "master" "gitlego" 1336233741
_gitlego246 = """#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import subprocess
import sys
import imp
def gitLegoLoader(command = None):
	if len(sys.argv) < 2 or sys.argv[1] != "git-lego": return
	gitLegoPath = os.path.join(os.path.realpath(os.path.expanduser("~") if os.path.expanduser("~") else os.path.dirname(__file__)), ".git-lego")
	if not os.path.isdir(gitLegoPath): os.mkdir(gitLegoPath)
	gitLegoDepPath = os.path.join(gitLegoPath, "https.github.com.blaizard.git.lego.git")
	if not os.path.isdir(gitLegoDepPath): subprocess.call(["git", "clone", "https://github.com/blaizard/git-lego.git", gitLegoDepPath])
	lib = imp.load_module("lib", None, os.path.join(gitLegoDepPath, "lib"), ('', '', imp.PKG_DIRECTORY))
	gitlego = lib.interface.Interface(__file__, cwd=gitLegoPath)
	sys.exit(gitlego.run(command) if command else gitlego.run(sys.argv[2:]))
"""
import imp
gitlego = imp.new_module("gitlego")
exec(_gitlego246, gitlego.__dict__)
## git-lego end
































## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" "temp1" 1221058638
_gitlego1347 = """#!/usr/bin/python
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
"""
import imp
temp1 = imp.new_module("temp1")
exec(_gitlego1347, temp1.__dict__)
## git-lego end



































# Tell me more!

## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" "temp2" 3106520206
_gitlego2231 = """#!/usr/bin/python
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
"""
import imp
temp2 = imp.new_module("temp2")
exec(_gitlego2231, temp2.__dict__)
## git-lego end

if __name__ == "__main__":

	gitLegoLoader()

	sys.exit(0)
