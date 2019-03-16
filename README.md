AnkiNotebooks 
===

Currently, this adds an Import option to Anki for Word documents in DOCX format.

Bullet lists within the Word document are converted to flashcards. This is so that you can
create a bunch of flash cards in Word, more quickly than typing them individually into Anki

The deepest list item becomes the back of the card. The path down becomes the front.

Example:
* ganglioglioma
  - intramedullary
    * ddx
      - ependymoma
      - astrocystoma
    * margins
      - circumscribed

becomes:

Front: ganglioglioma: intramedullary: ddx 

Back: ependymoma(line breaks) astrocystoma

Front: ganglioglioma: intramedullary: margins

Back: circumscribed


Export
------
Export to Word option added. Currently this simply functions like the export to tab separated text file, except it exports
as a bullet list in word.



TODO
----
- create a unique model for the cards and improve css styling
- word styling to html
- import media from word documents
- eventually option to sync word docs against collection
- support for odt
