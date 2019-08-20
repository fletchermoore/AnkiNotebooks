# not doing unit testing yet
# just so I don't have to launch Anki as I code


from doc_parser import parseXml, unzipDoc
from cards import genCards
import os

def getPath():
    currentDir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(currentDir, '../../sample_docs/spine 1.docx'))
    return path


def testParser():
    path = getPath()
    xmlContentStr = unzipDoc(path)
    if xmlContentStr != None:
        pathList = testMainParser(xmlContentStr)
        cards = genCards(pathList)
        printList(cards)



def testMainParser(xmlContentStr):
    return parseXml(xmlContentStr)

def printList(pathList):
    for path in pathList:
        print(str(path)) # path is a list of strings



testParser()