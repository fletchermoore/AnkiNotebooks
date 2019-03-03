
import xml.etree.ElementTree as ET
import re





# unused; delete?
def addLine(logStr, msg):
    return logStr + msg + "\n"


# stolen from stackoverflow
# fuck xml
def getNamespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''


# expects xml string read from docx file
# returns this structure, representing the document bullet lists
# [
#    ["path", "to", "terminal", "leaf"],
#    ["path", "to", "leaf2"],
#    ["path", "leaf3" ]
# ]
# reflecting a list in the document, which for example would look like
#     - path
#         * to
#             > terminal
#                 - leaf
#             > leaf2
#         * leaf3
def parseXml(xmlStr):
    root = ET.fromstring(xmlStr)
    # how to check this is valid?
    namespace = ""
    out = []
    currPath = []
    prevIndent = -1
    for child in root:
        namespace = getNamespace(child) #extract from body tag
        for grandchild in child: 
            # p tags
            currIndent, textContent = parseParagraph(grandchild, namespace)
            # am I going to be able to comprehend the following logic in a few years...?
            # adding paths to the output only if we are at a terminal leaf
            # we know we are at a terminal leaf because the previous indent is 
            # equal or greater. after the loop exits we add whatever is left over.
            if currIndent > prevIndent and currIndent > -1:
                currPath.append(textContent)
            elif currIndent == prevIndent and currIndent > 0:
                # if depth is at least 2 elements
                out = addPath(out, currPath, currIndent, prevIndent, textContent)
                currPath = currPath[0:-1] # remove the last string
                currPath.append(textContent) # replace with the new one
            elif currIndent == -1: # if paragraph, then not a part of list
                out = addPath(out, currPath, currIndent, prevIndent, textContent)
                currPath = [] # empty the path
            else: # currIndent is less than previous, but > -1
                out = addPath(out, currPath, currIndent, prevIndent, textContent)
                stepSize = (currIndent - prevIndent) - 1 # negative number result
                currPath = currPath[0:stepSize]
                currPath.append(textContent)
            prevIndent = currIndent # ready to loop
        out = addPath(out, currPath, currIndent, prevIndent, textContent)
    return out

# mostly for debugging
# appends currPath to allPaths and prints to terminal
def addPath(allPaths, currPath, currIndent, prevIndent, textContent):
    #print(currIndent, ': ', textContent, currPath, prevIndent)
    allPaths.append(currPath)
    return allPaths


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

# expect xml node for w:Pr
# returns int indent level value or -1
def parseIndentLevel(prXml, namespace):
    numPrTag = namespace + 'numPr'
    ilvlTag = namespace + 'ilvl'
    valAttr = namespace + 'val'
    for child in prXml:
        if child.tag == numPrTag:
            for grandchild in child:
                if grandchild.tag == ilvlTag:                    
                    valStr = grandchild.get(valAttr)
                    try:
                        return int(valStr)
                    except:
                        return -1
    return -1


# expects ET xml for w:p tag
# returns (int indentLevel, "textual content")
def parseParagraph(pChildXml, namespace):
    textContent = ""
    indentLevel = -1
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
    return (indentLevel, textContent)



