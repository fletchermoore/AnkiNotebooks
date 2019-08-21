
from zipfile import ZipFile, is_zipfile
import xml.etree.ElementTree as ET
import re, time, os
from .simple_docx.document import Document
from .simple_docx.paragraph import Paragraph
from .simple_docx.run import Run


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
# also returns image dict [filename] = blob for writing
def parseDocx(filename):
    doc = Document(filename)
    out = []
    images = {}
    currPath = []
    prevIndent = -1
    imagePrefix = gen_image_prefix(filename)

    for paragraph in doc.paragraphs:
        currIndent = paragraph.ilvl
        textContent, paragraphImages = toHtml(paragraph.runs, doc, imagePrefix)
        # add all the images to the masterlist
        # overwriting is OK, since we don't want to copy duplicate
        # images anyway        
        for filename in paragraphImages:
            images[filename] = paragraphImages[filename]
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

    return (out, images)

# expects a list of Run objects and Document object as well as a string
# that will be prefixed to all the image file names, unique to this import
# return html string concatination of the run object content
# and image dict { filename : blob }
def toHtml(runs, doc, imagePrefix):
    # for now, ignore images
    content = ""
    images = {}
    for run in runs:
        if run.type == "text":
            content += run.text
        elif run.type == "image":
            filename, blob = get_image(run.text, doc)
            if filename != None and blob != None:
                uniqueFilename = imagePrefix + filename
                content += f'<img src="{uniqueFilename}">'
                images[uniqueFilename] = blob
            else:
                content += '<img src="error.png">'
    return content, images


def addPath(allPaths, currPath, currIndent, prevIndent, textContent):
    allPaths.append(currPath)
    return allPaths


# expects rId and document
# rId is used to query blob from document
# we then get the filename in docx by rId as well
# return (filename, Blob) or (None, None) if failure
def get_image(rId, doc):
    blob = doc.get_image(rId)
    try:
        target = doc.rels[rId][1]
        filename = target.replace('/', '_')
        return (filename, blob)
    except:
        return (None, None)


# given file name of the docx file that is imported
# we will attach a timestamp and this will prefix individual image file names
def gen_image_prefix(filename):
    docx_name = os.path.splitext(os.path.basename(filename))[0]
    docx_name = docx_name.replace(' ', '_')
    ts = time.gmtime()
    prefix = docx_name + "_" + time.strftime("%Y-%m-%d-%Hh%Mm%Ss",ts) + "_"
    return prefix

