

# we'll essentially just do this like the existing CVS importer
# hopefully that works out just fine!

from anki.importing.noteimp import NoteImporter, ForeignNote
from aqt.utils import showInfo, showText, tooltip
from .doc_parser_exp import parseDocx
from .cards import genCards
import os


class DocImporter(NoteImporter):
    needDelimeter = False

    def __init__(self, *args):
        NoteImporter.__init__(self, *args)
        #self.lines = None
        self.fileobj = None
        #self.delimiter = None
        self.tagsToAdd = [] # ? do I need this too?
        self.imgList = {}

    
    # just add the media to the collection, no questions asked
    # called by run
    def importMedia(self):
        for filename in self.imgList:
            blob = self.imgList[filename]
            path = os.path.join(self.col.media.dir(), filename)
            if not os.path.exists(path):
                with open(path, "wb") as f:
                    f.write(blob)

    # parent run calls
    # c = foreignNotes()
    # and then importNotes(c)
    # we are going to add import media to the end for 
    def run(self):
        super().run() # call parent run
        self.importMedia()

    # ? requied inherited method
    # returns list of ForeignNotes, which get inserted by the parent class
    def foreignNotes(self):
        self.open()
        # process all lines
        # log = []
        notes = []

        if self.fileobj != None:
            pathList, self.imgList = parseDocx(self.file)
            cards = genCards(pathList)
            notes = cardsToForeignNotes(cards)
            #printList(cards)

        return notes

    # ? required by parent
    def open(self):
        "Parse the top line and determine the pattern and number of fields."
        # load & look for the right pattern
        self.cacheFile()

    def cacheFile(self):
        "Read file into self.lines if not already there."
        if not self.fileobj:
            self.openFile()

    def openFile(self):
        self.fileobj = self.file # just storing the file name instead of doing
                                    # any kind of file opening which is done in
                                    # parseDocx


    # ? required inherited method
    def fields(self):
        return 2


def cardsToForeignNotes(cards):
    # card shape is ('front', 'back')
    notes = []
    current_tags = []
    for card in cards:
        if card[0] == 'anki-tags':
            current_tags = card[1].split(' ')
        else:
            note = ForeignNote()
            note.fields = [ card[0], card[1] ]
            note.tags = current_tags
            notes.append(note)
    return notes


