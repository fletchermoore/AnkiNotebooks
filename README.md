AnkiNotebooks 
===

The ultimate goal of this project is so that I can quickly add and update
large sets of flashcards via Microsoft Word. You may find it helpful if you are studying
for medical school tests or the like, since creating the flashcards as I show
in my example is vastly faster than individually adding them to Anki. I can
almost create them real-time during a lecture (with some editing afterwards).

Currently, this is achieved by adding an Import and Export option to Anki for
Word documents (.docx). Bullet lists within the document become the cards. Other
text is ignored.

The deepest list item(s) becomes the back of the card. The path down becomes the front.

Example:
* ganglioglioma
  - intramedullary
    * ddx
      - ependymoma
      - astrocystoma
    * margins
      - circumscribed

becomes:

**Card 1**

ganglioglioma: intramedullary: ddx 

ependymoma  
astrocystoma

**Card 2**

ganglioglioma: intramedullary: margins

circumscribed


Import
------
For whatever reason when you initially import, Anki is perfectly happy to try to import a Word document as a CVS file. To use this addon, you must change the file
type to (.docx) in the file picker dialog before selecting the file.

Allow HTML must be checked or else you'll get escaped HTML in your cards. For now leave model as Basic and Field mappings as default. I will clean up all these options later.

Export
------
Adds a export option "Cards as Word document". This will currently perfectly reverse the import if the cards were created as in the example. For all other cards, the front of the card becomes the top level indent and the back becomes the second level indent.


Warning
-------
I have not yet extensively tested this. There are likely unancipated issues. It is working for me with my current version of Word (1902) on the latest OSX (as of 3/16/19) and Windows 10. 


TODO
----
- create a unique model for the cards and improve css styling
- word styling to html
- import media from word documents
- eventually option to sync word docs against collection
- support for odt (maybe never)
