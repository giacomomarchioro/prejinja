import pathlib
import time
import subprocess

currentState = {}
init = True

def CheckFolder(path,action):
    for i in pathlib.Path(path).iterdir():
        if i.is_file():
            if str(i) not in currentState:
                currentState[str(i)] = i.stat().st_mtime
                if not init:
                    action()
            else:
                if currentState[str(i)] != i.stat().st_mtime:
                    action()
                    currentState[str(i)] = i.stat().st_mtime

def CheckFile(filePath,action):
    i = pathlib.Path(filePath)
    if filePath not in currentState:
        currentState[filePath] = i.stat().st_mtime
        if not init:
            action()
    else:
        if currentState[filePath] != i.stat().st_mtime:
            action()
            currentState[filePath] = i.stat().st_mtime

def runPrejinjaGet():
    process = subprocess.Popen(['prejinjaget'])
    print("Running prejinjaget")

def runPrejinjaPut():
    process = subprocess.Popen(['prejinjaput'])
    print("Running prejinjaput")

while True:
    CheckFolder("srctemplates",runPrejinjaGet)
    CheckFile("translations.po.json",runPrejinjaPut)
    init = False
    time.sleep(3)

