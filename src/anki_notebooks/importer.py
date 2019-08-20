

# we'll essentially just do this like the existing CVS importer
# hopefully that works out just fine!

from anki.importing.noteimp import NoteImporter, ForeignNote
from aqt.utils import showInfo, showText, tooltip

from .doc_parser import parseXml, unzipDoc
from .cards import genCards


class DocImporter(NoteImporter):
    needDelimeter = False

    def __init__(self, *args):
        NoteImporter.__init__(self, *args)
        #self.lines = None
        self.fileobj = None
        #self.delimiter = None
        self.tagsToAdd = [] # ? do I need this too?


    # ? requied inherited method
    # returns list of ForeignNotes, which get inserted by the parent class
    def foreignNotes(self):
        self.open()
        # process all lines
        # log = []
        notes = []

        if self.fileobj != None:
            pathList = parseXml(self.fileobj)
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
        self.fileobj = unzipDoc(self.file)
        # self.dialect = None
        # self.fileobj = open(self.file, "r", encoding='utf-8-sig')
        # self.data = self.fileobj.read()
        # def sub(s):
        #     return re.sub("^\#.*$", "__comment", s)
        # self.data = [sub(x)+"\n" for x in self.data.split("\n") if sub(x) != "__comment"]
        # if self.data:
        #     if self.data[0].startswith("tags:"):
        #         tags = str(self.data[0][5:]).strip()
        #         self.tagsToAdd = tags.split(" ")
        #         del self.data[0]
        #     self.updateDelimiter()
        # if not self.dialect and not self.delimiter:
        #     raise Exception("unknownFormat")


    # ? required inherited method
    def fields(self):
        return 2

    # ? not required
    # def noteFromFields(self, fields):
    #     note = ForeignNote()
    #     note.fields.extend([x for x in fields])
    #     note.tags.extend(self.tagsToAdd)
    #     return note


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


