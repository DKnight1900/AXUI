
import os
import re
import sys
import unittest

import sys
sys.path.insert(0,"..")

def build_test_suite():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestSuite()
    for root, dirs, files in os.walk(current_dir):
        for file_ in files:
            if re.match("test_.*\.py$", file_) != None:
                sys.path.append(root)
                module = __import__(file_.split(".py")[0])
                suite.addTest(unittest.TestLoader().loadTestsFromModule(module))

    return suite

if __name__=="__main__":
    suite=build_test_suite()
    log_file = "unittest.log"
    with open(log_file, 'w') as f:
    	unittest.TextTestRunner(f).run(suite)
    
