#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "[branch=master]" "[namespace=gitlego]" [checksum=4269232004]
import imp
gitlego = imp.new_module("gitlego")
gitlego.__dict__["__file__"] = __file__
exec("""#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import imp, os, subprocess, sys
def loader(command = None):
	if len(sys.argv) < 2 or sys.argv[1] != "git-lego": return
	gitLegoPath = os.path.join(os.path.realpath(os.path.expanduser("~") if os.path.expanduser("~") else os.path.dirname(__file__)), ".git-lego")
	if not os.path.isdir(gitLegoPath): os.mkdir(gitLegoPath)
	gitLegoDepPath = os.path.join(gitLegoPath, "https.github.com.blaizard.git.lego.git")
	if not os.path.isdir(gitLegoDepPath): subprocess.call(["git", "clone", "https://github.com/blaizard/git-lego.git", gitLegoDepPath])
	lib = imp.load_module("lib", None, os.path.join(gitLegoDepPath, "lib"), ('', '', imp.PKG_DIRECTORY))
	gitlego = lib.interface.Interface(__file__, cwd=gitLegoPath)
	sys.exit(gitlego.run(command) if command else gitlego.run(sys.argv[2:]))
""", gitlego.__dict__)
## git-lego end

import lib, sys
def loader(command = None):
	gitlegoInstance = lib.interface.Interface(__file__, cwd="temp")
	gitlegoInstance.run(sys.argv[2:])
gitlego.loader = loader





## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "[branch=master]" "[namespace=temp1]" [checksum=3462859889]
import imp
temp1 = imp.new_module("temp1")
temp1.__dict__["__file__"] = __file__
exec("""#!/usr/bin/python
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
""", temp1.__dict__)
## git-lego end
# Tell me more!

## git-lego dep "https://github.com/blaizard/irapp.git" ".irapp/commands.py" "[branch=master]" "[namespace=temp2]" [checksum=4101715588]
import imp
temp2 = imp.new_module("temp2")
temp2.__dict__["__file__"] = __file__
exec("""#!/usr/bin/python
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
""", temp2.__dict__)
## git-lego end
if __name__ == "__main__":

	gitlego.loader()

	sys.exit(0)
