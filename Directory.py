import os

def makeCurDir():
    CurDir = os.path.dirname(__file__)
    ImgDir = CurDir +"\Image"
    return CurDir,ImgDir

def makeDir(dir):
    os.makedirs(dir, exist_ok=True)
