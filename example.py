#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "[branch=master]" "[namespace=gitlego]" [checksum=3765665242]
import imp
gitlego = imp.new_module("gitlego") if "gitlego" not in locals() else gitlego
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



import lib, sys, imp
def loader(command = None):
	gitlegoInstance = lib.interface.Interface(__file__, cwd="gitlego-loader-temp")
	gitlegoInstance.run(sys.argv[2:])
gitlego = imp.new_module("gitlegobypass")
gitlego.loader = loader



if __name__ == "__main__":

	gitlego.loader()

	sys.exit(0)
