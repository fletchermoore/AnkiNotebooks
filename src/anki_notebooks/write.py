

import os
import io
import zipfile
import shutil
import xml.etree.ElementTree as ET


def createDocument():
    contentTree = buildContentTree()
    contentTreeStr = ET.tostring(contentTree, encoding="UTF-8").decode("UTF-8")
    return getPrefix() + contentTreeStr + getPostfix()


def buildContentTree():
    p = ET.Element('w:p')
    r = ET.SubElement(p, 'w:r')
    t = ET.SubElement(r, 'w:t')
    t.text = "This is nothing but a test."
    return p




def writeDoc():   
    res = zip("blank10.docx") 


# modified from stack overflow
def make_zipfile(output_filename, source_dir, documentData):
    relroot = source_dir #os.path.abspath(os.path.join(source_dir, os.pardir))
    try:
        zip = zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED)
        print("after zip")
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                if not (file[0] == '.' and file != '.rels'): # exclude .DS_Store and who knows what
                    print(file)
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
    



def zip(filename):
    ankiNotebookDir = os.path.dirname(os.path.realpath(__file__))
    docFragPath = os.path.join(ankiNotebookDir, 'res', 'doc_frags')
    try:
        documentData = createDocument()
        print(documentData)
        make_zipfile(filename, docFragPath, documentData)
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