from anki.exporting import Exporter
from .write import writeDoc
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


    def createBullets(self):
        ids = sorted(self.cardIds())
        bullets = []
        def esc(s):
            # strip off the repeated question in answer if exists
            s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
            return self.escapeText(s)
        for cid in ids:
            c = self.col.getCard(cid)
            question = (0, esc(c.q()))
            bullets.append(question)
            answer = (1, esc(c.a()))
            bullets.append(answer)
        return bullets


    def cardIds(self):
        if not self.did:
            cids = self.col.db.list("select id from cards")
        else:
            cids = self.col.decks.cids(self.did, children=True)
        self.count = len(cids)
        return cids

    # from Exporter
    # def exportInto(self, path):
    #     self._escapeCount = 0
    #     file = open(path, "wb")
    #     self.doExport(file)
    #     file.close()

    # not called
    def doExport(self, file):
        ids = sorted(self.cardIds())
        strids = ids2str(ids)
        def esc(s):
            # strip off the repeated question in answer if exists
            s = re.sub("(?si)^.*<hr id=answer>\n*", "", s)
            return self.escapeText(s)
        out = ""
        for cid in ids:
            c = self.col.getCard(cid)
            out += esc(c.q())
            out += "\t" + esc(c.a()) + "\n"
        file.write(out.encode("utf-8"))