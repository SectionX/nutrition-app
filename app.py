################################################################
#This software is developed by <developer name> for <development reason>
#
#It's released under <LICENSE NAME> license.

# This file will launch the project_name/__main__.py script, including the line arguments.
# It can be used to test the imports and paths so the program can be safely installed
# as an excecutable.

import sys
import re
import os

sys.path.append(os.getcwd())


from project_name.__main__ import main
if __name__ == '__main__':
    sys.exit(main())