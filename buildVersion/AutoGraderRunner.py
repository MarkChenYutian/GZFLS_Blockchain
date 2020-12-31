import sys, os

main_version = sys.version_info[0]
if main_version != 3: raise Exception("Run Autograder with Python 3!")

minor_version = sys.version_info[1]
os.system("python AutoGrader.cpython-3{}.pyc".format(minor_version))