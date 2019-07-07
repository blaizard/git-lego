#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "master" "gitlego" 2123777180
_gitlego0 = """#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import subprocess
import sys
import imp
def loader(command = None):
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
gitlego.__dict__["__file__"] = __file__
exec(_gitlego0, gitlego.__dict__)
## git-lego end






































## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" "temp1" 172558474
_gitlego1 = """#!/usr/bin/python
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
temp1.__dict__["__file__"] = __file__
exec(_gitlego1, temp1.__dict__)
## git-lego end









































# Tell me more!

## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "master" "temp2" 1357810346
_gitlego2 = """#!/usr/bin/python
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
temp2.__dict__["__file__"] = __file__
exec(_gitlego2, temp2.__dict__)
## git-lego end







if __name__ == "__main__":

	gitlego.loader()

	sys.exit(0)
