# not doing unit testing yet
# just so I don't have to launch Anki as I code


from parser import unzipDoc, parseXml
import os
#testdir = os.path.dirname(__file__)
#srcdir = '../antigravity'
#sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

def testParser():
    currentDir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(currentDir, '../../sample_docs/spine 1.docx'))

    xmlContentStr = unzipDoc(path)
    if xmlContentStr != None:
        log = parseXml(xmlContentStr)
        print(log)

testParser()