# not doing unit testing yet
# just so I don't have to launch Anki as I code


from parser import unzipDoc, parseXml, printNamespace
import os

def getPath():
    currentDir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(currentDir, '../../sample_docs/spine 1.docx'))
    return path

def testFindNs(xmlContentStr):
    printNamespace(xmlContentStr)


def testParser():
    path = getPath()
    xmlContentStr = unzipDoc(path)
    if xmlContentStr != None:
        testMainParser(xmlContentStr)
        #testFindNs(xmlContentStr)

def testMainParser(xmlContentStr):
    log = parseXml(xmlContentStr)
    print(log)




testParser()