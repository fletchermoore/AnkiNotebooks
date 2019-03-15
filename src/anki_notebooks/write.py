

import os
import io
import zipfile
import shutil
import xml.etree.ElementTree as ET

# takes a list of tuples (ilvl, text)
# returns an xml string representing the document w:body content
def createDocument(bullets):
    xmlFrags = []
    for bullet in bullets:
        xmlFrags.append(listItemXml(bullet[0], 2, bullet[1]))
    xmlStr = joinElements(xmlFrags)
    return getPrefix() + xmlStr + getPostfix()


# takes a list of ET elements
# returns a single xml string
def joinElements(elemList):
    result = ''
    for elem in elemList:
        result += ET.tostring(elem, encoding="UTF-8").decode("UTF-8")
    return result


def paragraphXml(text):
    p = ET.Element('w:p')
    r = ET.SubElement(p, 'w:r')
    t = ET.SubElement(r, 'w:t')
    t.text = text
    return p

def emptyParagraphXml():
    return ET.Element('w:p')


# reference xml:
# <w:p w:rsidR="000308F2" w:rsidRDefault="000308F2" w:rsidP="000308F2">
#     <w:pPr>
#         <w:pStyle w:val="ListParagraph"/>
#         <w:numPr>
#             <w:ilvl w:val="1"/>
#             <w:numId w:val="1"/>
#         </w:numPr>
#     </w:pPr>
#     <w:r>
#         <w:t>second point</w:t>
#     </w:r>
# </w:p>
# 
# numId 1 is a numbered list, numId 2 is a bullet list
# this style is not intrinsic to word but defined by me in the 'numbering.xml' file
def listItemXml(depth, numId, text):
    p = ET.Element('w:p')
    pPr = ET.SubElement(p, 'w:pPr')
    pStyle = ET.SubElement(pPr, 'w:pStyle').set('w:val', 'ListParagraph')
    numPr = ET.SubElement(pPr, 'w:numPr')
    ilvl = ET.SubElement(numPr, 'w:ilvl').set('w:val', str(depth))
    numId = ET.SubElement(numPr, 'w:numId').set('w:val', str(numId))
    r = ET.SubElement(p, 'w:r')
    t = ET.SubElement(r, 'w:t')
    t.text = text
    return p


def writeDoc():   
    sampleContent = [
        (0, "this"),
        (1, "is"),
        (2, "my"),
        (3, "awesome"),
        (2, "document"),
        (1, "go home youre drunk")
    ]
    xml = createDocument(sampleContent)
    res = zip("blank10.docx", xml) 


# modified from stack overflow
def make_zipfile(output_filename, source_dir, documentData):
    relroot = source_dir #os.path.abspath(os.path.join(source_dir, os.pardir))
    try:
        zip = zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                if not (file[0] == '.' and file != '.rels'): # exclude .DS_Store and who knows what
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename): # regular files only
                        arcname = os.path.join(os.path.relpath(root, relroot), file)
                        if file == 'document.xml':
                            zip.writestr(arcname, documentData)
                        else:
                            zip.write(filename, arcname)
    except:
        print("opening zip failed")
        return None
    



def zip(filename, documentXml):
    ankiNotebookDir = os.path.dirname(os.path.realpath(__file__))
    docFragPath = os.path.join(ankiNotebookDir, 'res', 'doc_frags')
    try:
        make_zipfile(filename, docFragPath, documentXml)
        return True
    except:
        print("Failed to create .docx archive.")
        return None


# ElementTree does not create a document that word enjoys. So we will stitch together a
# document from a template blank word document. ET will be used to create the body content only.
def getPrefix():
    prefix = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" 
    xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" 
    xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" 
    xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" 
    xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" 
    xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" 
    xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" 
    xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" 
    xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" 
    xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" 
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
    xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" 
    xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" 
    xmlns:o="urn:schemas-microsoft-com:office:office" 
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
    xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" 
    xmlns:v="urn:schemas-microsoft-com:vml" 
    xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" 
    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" 
    xmlns:w10="urn:schemas-microsoft-com:office:word" 
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" 
    xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" 
    xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" 
    xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" 
    xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" 
    xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" 
    xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" 
    xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 w16se w16cid wp14">
    <w:body>
    """
    return prefix

def getPostfix():
    postfix = """
        <w:p w:rsidR="00717595" w:rsidRDefault="00717595">
            <w:bookmarkStart w:id="0" w:name="_GoBack"/>
            <w:bookmarkEnd w:id="0"/>
        </w:p>
        <w:sectPr w:rsidR="00717595" w:rsidSect="000B4652">
            <w:pgSz w:w="12240" w:h="15840"/>
            <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
            <w:cols w:space="720"/>
            <w:docGrid w:linePitch="360"/>
        </w:sectPr>
    </w:body>
</w:document>
    """
    return postfix