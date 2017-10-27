import os
UTIL_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIRECTORY = os.path.abspath(os.path.join(UTIL_DIRECTORY, os.pardir))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SCRIPTS_DIRECTORY, os.pardir))
DATA_DIRECTORY = ROOT_DIRECTORY + '/data'
