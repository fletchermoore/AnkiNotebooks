
import xml.etree.ElementTree as ET
from .xml import is_tag_match, get_attr_val
from .run import Run
import re

# sampleXml = """<w:p w14:paraId="6866CFFC" w14:textId="23B3221B" w:rsidR="008B6084" w:rsidRDefault="008B6084" w:rsidP="008B6084">
#             <w:pPr>
#                 <w:pStyle w:val="ListParagraph"/>
#                 <w:numPr>
#                     <w:ilvl w:val="1"/>
#                     <w:numId w:val="1"/>
#                 </w:numPr>
#             </w:pPr>
#             <w:r>
#                 <w:t>we</w:t>
#             </w:r>
#         </w:p>"""


class Paragraph:
    def __init__(self, elem):
        self.ilvl, self.runElems = self.parse(elem)
        # now process runs
        # ultimately you have a list of Run objects
        # Run objects can contain plain text or image references
        self.runs = self.parse_runs(self.runElems)
        
        #textContent += self.parse_run(child)

    # expects w:r xml element list
    # returns Run list
    def parse_runs(self, runElems):
        runs = []
        for runElem in runElems:
            runs.append(self.parse_run(runElem))
        return runs

    # expects ET xml for w:p tag
    # returns (int indentLevel, "textual content")
    def parse(self, pElem):
        runs = []
        indentLevel = -1
        for child in pElem:
            # either w:Pr, w:r, w:proofErr, w:gramErr
            if is_tag_match(child, '}r'): 
                runs.append(child)
            elif is_tag_match(child, '}pPr'):
                indentLevel = self.parse_indent_level(child)
            # ignore all other paragraph children for now
        return (indentLevel, runs)


        # expect xml node for w:Pr
    # returns int indent level value or -1
    def parse_indent_level(self, prXml):
        for child in prXml:
            if is_tag_match(child, 'numPr'):
                for grandchild in child:
                    if is_tag_match(grandchild, 'ilvl'):                    
                        valStr = get_attr_val(grandchild, 'val')
                        #grandchild.get(valAttr)
                        try:
                            return int(valStr)
                        except:
                            return -1
        return -1

    # expects xml node representing w:r element
    # returns Run object
    def parse_run(self, rXml):
        # as far as I know, possible children include w:t and w:lastRenderedPageBreak
        # I don't think its possible to have multiple t or drawing children 
        # but I am not sure.
        text = ""
        for child in rXml:
            if is_tag_match(child, '}t'):
                if child.text == "":
                    text += " " # a single blank space seems to be represented
                    # like <w:t xml:space="preserve"></w:t>
                else:
                    text += child.text
            elif is_tag_match(child, '}drawing'):
                return Run(self.parse_image_ref(child), "image")
        return Run(text)


    # expects xml node for w:drawing (which is usually a lot of garbage)
    # converts this node to string and then regex searches for rId\d+ to find
    # the image reference
    # returns rIdxxx string
    def parse_image_ref(self, drawingElem):
        pattern = re.compile('rId\d+')
        drawingRawXml = ET.tostring(drawingElem).decode()
        rId = pattern.search(drawingRawXml).group(0)
        return rId