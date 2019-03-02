# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showText, tooltip
# import all of the Qt GUI library
from aqt.qt import *

from .parser import unzipDoc, parseXml


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    path = openDoc()
    xmlContentStr = unzipDoc(path)
    if xmlContentStr != None:
        log = parseXml(xmlContentStr)
        showText(log)


def createDeck():
    dId = mw.col.decks.id("TEST DECK")
    mw.moveToState("deckBrowser") # is this safe to call anytime?
    # mw.deckBrowser.refresh() # will crash program if not on browser already

    # show a message box
    showInfo("Deck id: %d" % dId)

# create a new menu item, "test"
action = QAction("Run test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

# presents file picker and returns user filepath
def openDoc():
    # returns [str,str]
    tup = QFileDialog.getOpenFileName(mw, 'Choose File', mw.pm.base, "Open Document Files (*.docx)")
    return tup[0]
    # showInfo(str(path))


