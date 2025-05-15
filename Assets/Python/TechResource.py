from CvPythonExtensions import *
gc = CyGlobalContext()

## Customization Start ##

TechBonus = {
	"TECH_HORSEBACK_RIDING":[
        ["BONUS_HORSE", 25]
	],
	"TECH_METAL_CASTING":
    [
        ["BONUS_COPPER", 25],
        ["BONUS_IRON", 25]
	],
	"TECH_HERBALISM":[
		["BONUS_SPICES", 25]
	],
}

## Customization End ##
## Do Not Edit Below ##

def addBonus(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isAlive():
		iTech = pPlayer.getCurrentResearch()
		if iTech == -1: return
		iBonusRate = calculateModifier(iTech, iPlayer)
		iBonusResearch = pPlayer.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH) * iBonusRate/100
		gc.getTeam(pPlayer.getTeam()).changeResearchProgress(iTech, iBonusResearch, iPlayer)

def calculateModifier(iTech, iPlayer):
	iBonusRate = 0
	sTechType = gc.getTechInfo(iTech).getType()
	if sTechType in TechBonus:
		for (sBonus, iRate) in TechBonus[sTechType]:
			iBonus = gc.getInfoTypeForString(sBonus)
			if iBonus > -1:
				if gc.getPlayer(iPlayer).getNumAvailableBonuses(iBonus) > 0:
					iBonusRate += iRate
	return iBonusRate