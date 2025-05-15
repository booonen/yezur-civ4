import BugEventManager
import BugGameUtils

from CvPythonExtensions import *
import sys
import CvUtil
gc = CyGlobalContext()

def init():
    em = BugEventManager.g_eventManager
    em.addEventHandler("GameStart", onGameStart)

def onGameStart(argsList):
    print "YEZUR Super Forts"
    CyMap().calculateCanalAndChokePoints()
    