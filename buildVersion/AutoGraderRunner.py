import sys, os

main_version = sys.version_info[0]
if main_version != 3: raise Exception("Run Autograder with Python 3!")

minor_version = sys.version_info[1]
if minor_version == 5:
    os.system("python AutoGrader.cpython-35.pyc")
if minor_version == 6:
    os.system("python AutoGrader.cpython-36.pyc")
if minor_version == 7:
    os.system("python AutoGrader.cpython-37.pyc")
if minor_version == 8:
    os.system("python AutoGrader.cpython-38.pyc")
if minor_version == 9:
    os.system("python AutoGrader.cpython-39.pyc")