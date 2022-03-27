#!/usr/bin/python

import subprocess, os

str_reset = '\u001b[0m'
str_black = '\u001b[40m\u001b[37m'
str_white = '\u001b[47;1m\u001b[30m'

def getchar():
   #Returns a single character from standard input
   ### unix version
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch
   ### --unix version


def changeSBrightness(value):
    os.system("xrandr --output eDP1 --brightness " + str(value))

def changeHBrightness(value):
    os.system("sudo light -S " + str(value * 100))


def getHardBrightness():
    result = subprocess.run(['light'], stdout=subprocess.PIPE, text=True)
    return float(result.stdout) / 100

def getSoftBrightness():
    result = subprocess.run(['xrandr', '--verbose', '--current'], stdout=subprocess.PIPE, text=True)

    # print(type(result.stdout))
    brightness = 0
    for line in result.stdout.split('\n'):
        if line.lower().find("brightness: ") > -1:
            brightness = float(line.lower().split("brightness: ")[1])
            break
    return brightness

cher = ""
helpInfo = "q: quit\nn, o: switch mode\ne, i: -/+ value\nE, I: min/max\n"

sfMode = False

def colorize(line, mode):
    if mode:
        return str_white + line + str_reset
    return line

brFunction = (getHardBrightness, changeHBrightness)

def changeBrDelta(value):
    brVal = brFunction[0]()
    brVal += value
    if brVal <= 0.0: brVal = 0.01
    if brVal > 1.0: brVal = 1
    brFunction[1](brVal)

def setMax():
    brFunction[1](1)

def setMin():
    brFunction[1](0.1)


while cher != 'q':
    if cher == 'n' or cher == 'o':
        sfMode = not sfMode
        if sfMode:
            brFunction = (getSoftBrightness, changeSBrightness)

        else:
            brFunction = (getHardBrightness, changeHBrightness)
    elif cher == 'e':
        changeBrDelta(-0.05)
    elif cher == 'i':
        changeBrDelta(0.05)
    elif cher == 'I':
        setMax()
    elif cher == 'E':
        setMin()



    os.system('clear')
    print(helpInfo)
    print(colorize("Soft mode", sfMode) + " " + colorize("Hard mode", not sfMode))
    brightnessLine = "  " + str(int(getSoftBrightness() * 100) / 100)
    brightnessLine = brightnessLine + " " * (10 - len(brightnessLine)) + str(getHardBrightness())
    print(brightnessLine)
    cher = getchar()

# print(result.stdout)
