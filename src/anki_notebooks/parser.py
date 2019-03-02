from zipfile import ZipFile, is_zipfile
import xml.etree.ElementTree as ET
import re


# returns string representing content of docx internal file document.xml or None on failure
# given string path to a .docx file
def unzipDoc(path):
    if is_zipfile(path) == False:
        showInfo('Unable to open selected file (filepath not found).')
        return None
    z = None
    doc = None
    try:
        z = ZipFile(path)
        doc = z.read('word/document.xml')
        # is this closed properly on failure?
    except:
        showInfo('Unable to open selected file (unzip/read failed).')
    #    print 'failed to open zip file or read \'content.xml\''
        z.close()
        return None
    z.close()
    return doc


def addLine(logStr, msg):
    return logStr + msg + "\n"


# stolen from stackoverflow
# fuck xml
def getNamespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''


# does not work; delete later
def printNamespace(xmlStr):
    root = ET.fromstring(xmlStr)
    # assume we are the document tag
    print("Finding namespace...")
    print(root.attrib)
    #print(root.get('xmlns:w'))


# expects xml string read from docx file
# return parsed content string (currently nebulus)
def parseXml(xmlStr):
    root = ET.fromstring(xmlStr)
    # how to check this is valid?
    
    namespace = ""
    out = ""
    for child in root:
        namespace = getNamespace(child)
        out = addLine(out, child.tag) # body tag
        for grandchild in child: 
            # p tags
            paragraphText = parseParagraph(grandchild, namespace)
            out = addLine(out, paragraphText)
    return out


# current unused
# expects namespaced tag name like {really-long-string}p
# returns unnamespaced tag name like p
def shortTag(nsTag):
    frags = nsTag.split('}')
    return frags[-1:][0] # safe since split will always return a list of at least 1 string


# expects xml node representing w:r element
# returns string of text contents
def rText(rXml, namespace):
    # as far as I know, possible children include w:t and w:lastRenderedPageBreak
    text = ""
    tTag = namespace + 't'
    for child in rXml:
        if child.tag == tTag:
            text += child.text
    return text

# except xml node for w:Pr
# returns indent level or None
def parseIndentLevel(prXml, namespace):
    numPrTag = namespace + 'numPr'
    ilvlTag = namespace + 'ilvl'
    valAttr = namespace + 'val'
    for child in prXml:
        if child.tag == numPrTag:
            for grandchild in child:
                if grandchild.tag == ilvlTag:                    
                    return grandchild.get(valAttr)
    return None


# expects ET xml for w:p tag
# returns text content
def parseParagraph(pChildXml, namespace):
    textContent = ""
    indentLevel = None
    rTag = namespace + 'r'
    pPrTag = namespace + 'pPr'
    for child in pChildXml:
        tag = child.tag
        # either w:Pr, w:r, w:proofErr, w:gramErr
        if tag == rTag: 
            textContent += rText(child, namespace)
        elif tag == pPrTag:
            indentLevel = parseIndentLevel(child, namespace)
        # ignore all other paragraph children for now
    if indentLevel == None:
        return textContent
    else:
        return str(indentLevel) + ': ' + textContent


