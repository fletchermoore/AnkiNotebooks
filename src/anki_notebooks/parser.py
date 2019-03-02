from zipfile import ZipFile, is_zipfile
import xml.etree.ElementTree as ET


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


# expects xml string read from docx file
# return parsed content string (currently nebulus)
def parseXml(xmlStr):
    root = ET.fromstring(xmlStr)
    # how to check this is valid?
    
    out = ""
    for child in root:
        out = addLine(out, child.tag) # body tag
        for grandchild in child: 
            # p tags
            paragraphText = parseParagraph(grandchild)
            out = addLine(out, paragraphText)
    return out


# expects namespaced tag name like {really-long-string}p
# returns unnamespaced tag name like p
def shortTag(nsTag):
    frags = nsTag.split('}')
    return frags[-1:][0] # safe since split will always return a list of at least 1 string


# expects xml node representing w:r element
# returns string of text contents
def rText(rXml):
    # as far as I know, possible children include w:t and w:lastRenderedPageBreak
    text = ""
    for child in rXml:
        if shortTag(child.tag) == 't':
            text += child.text
    return text


# expects ET xml for w:p tag
# returns text content
def parseParagraph(pChildXml):
    preamble = "presumed w:p contents: "
    textContent = ""
    for child in pChildXml:
        tag = shortTag(child.tag)
        # either w:Pr, w:r, w:proofErr, w:gramErr
        if tag == 'r': 
            textContent += rText(child)
        # ignore all other paragraph children for now
    return preamble + textContent


