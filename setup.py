from distutils.core import setup
import py2exe

# for the version with the console
# setup(console=['guiJwent.py'])

# for a purely gui version
setup(windows = [{'script': "guiJwent.py"}])

# C:\Users\Jeff\PycharmProjects\funstuff\games\jwent>python setup.py py2exe --includes sip