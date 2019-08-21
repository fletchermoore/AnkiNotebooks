

from zipfile import ZipFile, is_zipfile
import xml.etree.ElementTree as ET
from .xml import is_tag_match
from .paragraph import Paragraph
#import re


class Document:
    def __init__(self, path):

        self.docXml = ""
        self.relsXml = ""
        self.paragraphs = []
        self.mediaFiles = {}
        self.rels = {}

        self.load(path)

        if self.is_loaded():
            self.paragraphs = self.parse_paragraphs(self.docXml)
            self.rels = self.build_rel_dict(self.relsXml)


    def load(self, path):
        """ reads files from docx
        reads document.xml to docXml
        reads document.xml.rels to relsXml
        reads word/media folder files to mediaFiles """
        if is_zipfile(path) != False:
            try:
                z = ZipFile(path)
                # extract relevant xml
                self.docXml = z.read('word/document.xml')
                self.relsXml = z.read('word/_rels/document.xml.rels')
                # extract media
                names = z.namelist()
                for name in names:
                    if name.startswith('word/media/'):
                        filename = name[5:] # remove "word/"
                        self.mediaFiles[filename] = z.read(name)
                z.close()
            except:
                z.close()


    def is_loaded(self):
        return self.docXml != ""


    def parse_paragraphs(self, xml):
        paragraphs = []
        root = ET.fromstring(xml) # w:document
        for child in root: # w:body, could it be something else?
            for grandchild in child: # children could be p or sections stuff
                if is_tag_match(grandchild, 'p'):
                    paragraphs.append(Paragraph(grandchild))
        return paragraphs


    def build_rel_dict(self, xml):
        rels = {}
        root = ET.fromstring(xml) # Relationships
        for child in root:
            if is_tag_match(child, '}Relationship'):
                rId = child.get('Id')
                rType = child.get('Type')
                target = child.get('Target')
                rels[rId] = (rType, target)
        return rels


    # given rId, probably from a run, return the image file
    # if keyError (not found) return None
    def get_image(self, rId):
        try:
            target = self.rels[rId][1]
            return self.mediaFiles[target]
        except:
            return None






                

        

        