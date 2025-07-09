import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from categories.Category import Category
from categories.Set import Set
from categories.Graph import grph
from categories.Group import grp, Operation
from categories.TopologicalSpace import top
from categories.MeasurableSpace import meas

class TestCategories(unittest.TestCase):
    ## Category Module Tests

    ### Object Class Tests

    ### Morphism Class Tests

    ### Category Class Tests

    ### IdentityMorphism Class Tests

    ### Functors Class Tests



    ## Set Module Tests 

    ### Set Class Tests

    ### Function Class Tests



    ## Graph Module Tests

    ### Graph Class Tests



    ## Group Module Tests
 
    ### Operation Class Tests
    def add_mod_3(self,a, b):
        return (a + b) % 3
    ### Grp Class Tests
    def testGrp(self):
        s = Set([0, 1, 2])
        op = Operation(self.add_mod_3)
        g = grp(s, identity=0, operation=op)
        self.assertEqual(g.X, [0, 1, 2])
        self.assertEqual(g.identity, 0)
        self.assertEqual(g.operation.apply(1, 2), 0) 



    ## TopologicalSpace Module Tests
    def testTop(self):
        s = Set([0, 1])
        open_sets = [[], [0], [0, 1]]
        t = top(s, open_sets)
        self.assertEqual(t.X, [0, 1])
        self.assertEqual(t.topology, open_sets)
        
    ### Top class tests



    ## MeasurableSpace Module Tests

    ### Meas Class Tests



if __name__ == '__main__':
    unittest.main()