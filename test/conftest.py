import os
import sys

def absjoin(*pieces):
    return os.path.abspath(os.path.join(*pieces))

DIRNAME = os.path.normpath(os.path.dirname(__file__))

ROOT = absjoin(DIRNAME, '..')

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
