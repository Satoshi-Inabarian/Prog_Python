import os
import sys

def checkfile(Imgfile):
    DirFlag = os.path.exists(Imgfile)
    if DirFlag == False:
        print("Can't find the following file",Imgfile)
        sys.exit()
    
def makeDir(dir):
    DirFlag = os.path.exist(dir)
    if DirFlag == False: 
        os.mkdir(dir)