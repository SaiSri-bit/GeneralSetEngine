import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from categories.Set import Set
from categories.Graph import grph
from categories.Group import grp
from categories.TopologicalSpace import top

class Cayley(grph):
    pass