import BugEventManager
import BugGameUtils

from CvPythonExtensions import *
import sys
import CvUtil
gc = CyGlobalContext()

import GreatPeopleScreen

def init():
    em = BugEventManager.g_eventManager
    em.addEventHandler("greatPersonBorn", onGreatPersonBorn)

def onGreatPersonBorn(argsList):
    pUnit, iPlayer, pCity = argsList
    if pUnit.isNone() or pCity.isNone():
        return
    ## Great People Movie ##
    if not CyGame().isNetworkMultiPlayer() and iPlayer == CyGame().getActivePlayer():
        GreatPeopleScreen.GreatPeopleScreen().interfaceScreen(pUnit, iPlayer)
    ## Great People Movie ##
    