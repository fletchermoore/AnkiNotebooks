from anki.exporting import Exporter
from .write import writeDoc
from .paths import escapedCardToPath, pathsToBullets
import re

class DocExporter(Exporter):

    key = _("Cards as Word Document")
    ext = ".docx"

    def __init__(self, col):
        Exporter.__init__(self, col)

    def exportInto(self, path):
        self.count = 0 # required for success prompt
        bullets = self.createBullets()
        writeDoc(path, bullets)


    def escapeText(self, text):
        "Escape newlines, tabs, CSS."
        # fixme: we should probably quote fields with newlines
        # instead of converting them to spaces
        text = text.replace("\n", " ")
        text = text.replace("\t", " " * 8)
        text = re.sub("(?i)<style>.*?</style>", "", text)
        text = re.sub(r"\[\[type:[^]]+\]\]", "", text)
        # if "\"" in text:
        #     text = "\"" + text.replace("\"", "\"\"") + "\""
        return text


    def createBullets(self):
        ids = sorted(self.cardIds())
        def esc(s):
            # strip off the repeated question in answer if exists
            s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
            return self.escapeText(s)
        paths = []
        for cid in ids:
            c = self.col.getCard(cid)            
            question = esc(c.q())            
            answer = esc(c.a())
            path = escapedCardToPath(question, answer)
            paths.append(path)
        bullets = pathsToBullets(paths)
        return bullets


    def cardIds(self):
        if not self.did:
            cids = self.col.db.list("select id from cards")
        else:
            cids = self.col.decks.cids(self.did, children=True)
        self.count = len(cids)
        return cids

