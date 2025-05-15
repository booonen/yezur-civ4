import CvUtil
import CvScreenEnums
from CvPythonExtensions import *
gc = CyGlobalContext()

class GreatPeopleScreen:

	def __init__(self):
		self.GreatPeople = {	"UNIT_PROPHET": "[ICON_RELIGION]",
					"UNIT_ARTIST": "[ICON_CULTURE]",
					"UNIT_SCIENTIST": "[ICON_RESEARCH]",
					"UNIT_MERCHANT": "[ICON_GOLD]",
					"UNIT_ENGINEER": "[ICON_PRODUCTION]",
					"UNIT_GREAT_GENERAL": "[ICON_STRENGTH]",
					"UNIT_GREAT_SPY": "[ICON_ESPIONAGE]"}
				
	def interfaceScreen(self, pUnit, iPlayer):
		screen = CyGInterfaceScreen("Great People Screen", CvScreenEnums.GREAT_PEOPLE_SCREEN)
		if CyGame().isPitbossHost(): return
		sUnitName = pUnit.getNameNoDesc()
		if sUnitName == "": return

		self.W_MAIN_PANEL = screen.getXResolution() * 3/4
		self.H_MAIN_PANEL = screen.getYResolution() * 7/10
		self.X_MAIN_PANEL = (screen.getXResolution()/2) - (self.W_MAIN_PANEL/2)
		self.Y_MAIN_PANEL = 70
		
		self.iMarginSpace = 15
		
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - self.iMarginSpace * 2
		self.H_HEADER_PANEL = self.H_MAIN_PANEL/3
		
		self.X_TITLE_TEXT = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_TITLE_TEXT = self.Y_HEADER_PANEL + 12
		self.W_TITLE_TEXT = self.W_HEADER_PANEL - self.iMarginSpace * 2
		self.H_TITLE_TEXT = 64

		self.X_QUOTE = self.X_TITLE_TEXT
		self.Y_QUOTE = self.Y_TITLE_TEXT + self.H_TITLE_TEXT + self.iMarginSpace
		self.W_QUOTE = self.W_TITLE_TEXT
		self.H_QUOTE = self.H_HEADER_PANEL - self.H_TITLE_TEXT - self.iMarginSpace * 3
		
		self.W_EXIT = 120
		self.H_EXIT = 30
		self.X_EXIT = (screen.getXResolution() - self.W_EXIT) /2
		self.Y_EXIT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL - self.H_EXIT - self.iMarginSpace
		
		self.X_LEADER_ICON = self.X_TITLE_TEXT
		self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace
		self.H_LEADER_ICON = self.Y_EXIT - self.Y_LEADER_ICON - self.iMarginSpace
		self.W_LEADER_ICON = self.H_LEADER_ICON
		
		self.X_TEXT_PANEL = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_LEADER_ICON
		self.W_TEXT_PANEL = self.W_HEADER_PANEL - self.W_LEADER_ICON - self.iMarginSpace * 2
		self.H_TEXT_PANEL = self.H_LEADER_ICON

		iType = pUnit.getUnitType()
		Info = gc.getUnitInfo(iType)
		sGreat = ""
		for i in xrange(Info.getNumUnitNames()):
			sName = Info.getUnitNames(i)
			if CyTranslator().getText(sName, ()) == sUnitName:
				sGreat = sName[8:]
				break

		if sGreat:
			sButton = ""
			sIcon = "[ICON_STAR]"
			sArtDef = CyArtFileMgr().getInterfaceArtInfo("ART_DEF_" + sGreat)
			if sArtDef:
				sButton = sArtDef.getPath()
			sQuote = CyTranslator().getText("TXT_KEY_" + sGreat + "_QUOTE", ())
			sPedia = CyTranslator().getText("TXT_KEY_" + sGreat + "_PEDIA", ())
			sType = Info.getType()
			if sType in self.GreatPeople:
				sIcon = self.GreatPeople[sType]
		else:
			return

		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground(False)
		
		screen.addPanel("MainPanel", "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		screen.addPanel("TitlePanel", "", "", true, false, self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM)
		screen.addPanel("PediaPanel", "", "", true, true, self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_MAIN)
		screen.setStyle("PediaPanel", "Panel_TechDiscover_Style")
		screen.addDDSGFC("TechSplashIcon", sButton, self.X_LEADER_ICON, self.Y_LEADER_ICON, self.W_LEADER_ICON, self.H_LEADER_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szNameText = "<color=255,255,0,255>" + u"<font=4b>" + CyTranslator().getText(sIcon, ()) + Info.getDescription().upper() + CyTranslator().getText(sIcon, ())
		szNameText += "\n" + sUnitName.upper() + u"</font>"
		screen.addMultilineText("NameText", szNameText, self.X_TITLE_TEXT, self.Y_TITLE_TEXT, self.W_TITLE_TEXT, self.H_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.addMultilineText("QuoteText", sQuote, self.X_QUOTE, self.Y_QUOTE, self.W_QUOTE, self.H_QUOTE, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.addMultilineText("PediaText", sPedia, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace, self.W_TEXT_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setButtonGFC("Exit", CyTranslator().getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
	def handleInput( self, inputClass ):
		return 0
	
	def update(self, fDelta):
		return