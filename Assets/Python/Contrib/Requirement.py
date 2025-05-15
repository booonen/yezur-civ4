import BugEventManager
import BugGameUtils

from CvPythonExtensions import *
import sys
import CvUtil
gc = CyGlobalContext()
lUnits = []
lBuildings = []
lProjects = []
bLoaded = False

def init():
    em = BugEventManager.g_eventManager
    em.addEventHandler("GameStart", onGameStart)
    em.addEventHandler("OnLoad", onLoadGame)
    BugGameUtils.addHandler(cannotTrain)
    BugGameUtils.addHandler(cannotConstruct)

def onLoadGame(argsList):
    print "YEZUR Game Load"
    loadEvents()
    
def onGameStart(argsList):
    print "YEZUR Game Start"
    loadEvents()
    
def cannotTrain(argsList):
    pCity = argsList[0]
    eUnit = argsList[1]
    bContinue = argsList[2]
    bTestVisible = argsList[3]
    bIgnoreCost = argsList[4]
    bIgnoreUpgrades = argsList[5]
    print "YEZUR cannot train called"
    return max(False, checkRequirements(eUnit, 0, pCity, pCity.getOwner()))
    
def cannotConstruct(argsList):
    pCity = argsList[0]
    eBuilding = argsList[1]
    bContinue = argsList[2]
    bTestVisible = argsList[3]
    bIgnoreCost = argsList[4]
    return max(False, checkRequirements(eBuilding, 1, pCity, pCity.getOwner()))
    
def checkRequirements(iItem, iType, pCity, iOwner):
	List = lUnits
	if iType == 1:
		List = lBuildings
	elif iType == 2:
		List = lProjects
	pPlayer = gc.getPlayer(iOwner)
	for item in List:
		for i in item[0]:
			if iItem != i: continue
			if len(item[1]):
				bORCivic = False
				for j in item[1]:
					if pPlayer.isCivic(j): bORCivic = True
				if not bORCivic: return True
			if pCity.getPopulation() < item[2]: return True
			if pCity.getCultureLevel() < item[3]: return True
			if item[14] and not pCity.plot().isHills(): return True
			if pCity.plot().calculateCulturePercent(iOwner) < item[15]: return True
			if item[16] and not gc.getTeam(pPlayer.getTeam()).getAtWarCount(True): return True
			if item[17] and gc.getTeam(pPlayer.getTeam()).getAtWarCount(True): return True
			for iBuilding in item[18]:
				if pCity.isHasBuilding(iBuilding): return True
			bHills = False
			bPeak = False
			bANDTerrain = False
			bANDFeature = False
			bANDBonus = False
			bANDImprovement = False
			bORTerrain = False
			bORFeature = False
			bORBonus = False
			bORImprovement = False
			for i in xrange(21):
				pPlot = pCity.getCityIndexPlot(i)
				if pPlot.isNone(): continue
				if pPlot.getOwner() != iOwner: continue
				if pPlot.isHills(): bHills = True
				if pPlot.isPeak(): bPeak = True
				if pPlot.getTerrainType() == item[6]: bANDTerrain = True
				for j in item[7]:
					if pPlot.getTerrainType() == j: bORTerrain = True
				if pPlot.getFeatureType() == item[8]: bANDFeature = True
				for j in item[9]:
					if pPlot.getFeatureType() == j: bORFeature = True
				if pPlot.getBonusType(-1) == item[10]: bANDBonus = True
				for j in item[11]:
					if pPlot.getBonusType(-1) == j: bORBonus = True
				if pPlot.getImprovementType() == item[10]: bANDImprovement = True
				for j in item[13]:
					if pPlot.getImprovementType() == j: bORImprovement = True
			if item[4] and not bHills: return True
			if item[5] and not bPeak: return True
			if item[6] > -1 and not bANDTerrain: return True
			if len(item[7]) and not bORTerrain: return True
			if item[8] > -1 and not bANDFeature: return True
			if len(item[9]) and not bORFeature: return True
			if item[10] > -1 and not bANDBonus: return True
			if len(item[11]) and not bORBonus: return True
			if item[12] > -1 and not bANDImprovement: return True
			if len(item[13]) and not bORImprovement: return True
	return False		

def getItem(sName):
	iItem = gc.getInfoTypeForString(sName)
	if iItem == -1:
		return [-1, []]
	lItems = []
	if sName.find("UNIT_") == 0:
		return [0, [iItem]]
	elif sName.find("UNITCLASS_") == 0:
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).getUnitClassType() == iItem:
				lItems.append(i)
		return [0, lItems]
	elif sName.find("SPECIALUNIT_") == 0:
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).getSpecialUnitType() == iItem:
				lItems.append(i)
		return [0, lItems]
	elif sName.find("BUILDING_") == 0:
		return [1, [iItem]]
	elif sName.find("BUILDINGCLASS_") == 0:
		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(i).getBuildingClassType() == iItem:
				lItems.append(i)
		return [1, lItems]
	elif sName.find("SPECIALBUILDING_") == 0:
		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(i).getSpecialBuildingType() == iItem:
				lItems.append(i)
		return [1, lItems]
	elif sName.find("PROJECT_") == 0:
		return [2, [iItem]]
	return [-1, []]
	
def loadEvents():
	sFilePath = "Mods/Yezur/Assets/XML/CustomXML/Requirement.xml"
	del lUnits[:]
	del lBuildings[:]
	del lProjects[:]
	MyFile=open(sFilePath)
	CurEvent = []
	for sCurrent in MyFile.readlines():
		if "#" in sCurrent: continue
		if "<Item>" in sCurrent:
			Item = getItem(CutString(sCurrent))
			if Item[0] == -1 or len(Item[1]) == 0:
				CurEvent = []
			else:
				##	iItemID, Civic, Population, CultureLevel, Hills, Peak, Terrain, Feature, Bonus, Improvement, BuiltOnHills, Nationality, War, Peace, AntiBuilding
				CurEvent = [Item[1], [], 0, -1, 0, 0, -1, [], -1, [], -1, [], -1, [], 0, 0, 0, 0, []]
		if len(CurEvent) == 0: continue
		if "<CivicType>" in sCurrent:
			iType = gc.getInfoTypeForString(CutString(sCurrent))
			if iType > -1:
				CurEvent[1].append(iType)
		elif "<iMinPopulation>" in sCurrent:
			CurEvent[2] = int(CutString(sCurrent))
		elif "<MinCultureLevel>" in sCurrent:
			CurEvent[3] = gc.getInfoTypeForString(CutString(sCurrent))
		elif "<bVicinityHills>" in sCurrent:
			CurEvent[4] = int(CutString(sCurrent))
		elif "<bVicinityPeak>" in sCurrent:
			CurEvent[5] = int(CutString(sCurrent))
		elif "<PrereqVicinityTerrain>" in sCurrent:
			CurEvent[6] = gc.getInfoTypeForString(CutString(sCurrent))
		elif "<TerrainType>" in sCurrent:
			iType = gc.getInfoTypeForString(CutString(sCurrent))
			if iType > -1:
				CurEvent[7].append(iType)
		elif "<PrereqVicinityFeature>" in sCurrent:
			CurEvent[8] = gc.getInfoTypeForString(CutString(sCurrent))
		elif "<FeatureType>" in sCurrent:
			iType = gc.getInfoTypeForString(CutString(sCurrent))
			if iType > -1:
				CurEvent[9].append(iType)
		elif "<PrereqVicinityBonus>" in sCurrent:
			CurEvent[10] = gc.getInfoTypeForString(CutString(sCurrent))
		elif "<BonusType>" in sCurrent:
			iType = gc.getInfoTypeForString(CutString(sCurrent))
			if iType > -1:
				CurEvent[11].append(iType)
		elif "<PrereqVicinityImprovement>" in sCurrent:
			CurEvent[12] = gc.getInfoTypeForString(CutString(sCurrent))
		elif "<ImprovementType>" in sCurrent:
			iType = gc.getInfoTypeForString(CutString(sCurrent))
			if iType > -1:
				CurEvent[13].append(iType)
		elif "<bBuiltOnHills>" in sCurrent:
			CurEvent[14] = int(CutString(sCurrent))
		elif "<iMinNationalityRatio>" in sCurrent:
			CurEvent[15] = int(CutString(sCurrent))
		elif "<bWar>" in sCurrent:
			CurEvent[16] = int(CutString(sCurrent))
		elif "<bPeace>" in sCurrent:
			CurEvent[17] = int(CutString(sCurrent))
		elif "<BuildingType>" in sCurrent:
			lAntiList = getItem(CutString(sCurrent))
			if lAntiList[0] == 1:
				for i in lAntiList[1]:
					if i in CurEvent[18]: continue
					CurEvent[18].append(i)
		elif "</Event>" in sCurrent:
			if Item[0] == 0:
				lUnits.append(CurEvent)
			elif Item[0] == 1:
				lBuildings.append(CurEvent)
			elif Item[0] == 2:
				lProjects.append(CurEvent)
			CurEvent = []
	bLoaded = True
	MyFile.close()

def CutString(string):   
	string = string[string.find(">") + 1:]
	string = string[:string.find("<")]
	return string