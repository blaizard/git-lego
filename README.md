# git-lego

Adds git functionality to a single file.
This utility allow to pick specific files from various git repositories and incorporate them into a single file.
This can be usefull if you share common routines with various scripts that are intended to be shared as a single file for example.

## Getting started

### Python

Add the following line of code to your python script:

```python
## git-lego dep "https://github.com/blaizard/git-lego.git" "loader.py" "master" "gitlego"
import imp
gitlego = imp.new_module("gitlego")
exec("""#!/usr/bin/python
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
""", gitlego.__dict__)
## git-lego end
```

and make sure this function is called before any command line parser in your main as follow:
```python
gitlego.loader()	
```

In order to import new files in your script, simply add the following line:
```python
## git-lego dep <git repo> <path> <branch> <namespace>
```

Then you can use the following command:
```bash
python myPythonScrypt.py git-lego update # Update the dependencies
python myPythonScrypt.py git-lego status # Gives the status of file dependencies
python myPythonScrypt.py git-lego commit -m "My git-lego commit!" # Commit local changes from the dependencies
```
