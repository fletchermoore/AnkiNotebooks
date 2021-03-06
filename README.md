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

* anki-tags
  - neuro peds tumors
* ganglioglioma
  - intramedullary
    * ddx
      - ependymoma
      - astrocystoma
    * margins
      - circumscribed
    * << pediatric brain mass that presents with temporal lobe epilepsy

becomes:

**Card 1**

ganglioglioma: intramedullary: ddx 

ependymoma  
astrocystoma

**Card 2**

ganglioglioma: intramedullary: margins

circumscribed

**Card 3**

pediatric brain mass that presents with temporal lobe epilepsy

ganglioglioma: intramedullary


Markup
------
If the deepest item starts with "<<", the generated card
will be reversed, as Card 3 above.

If you create a pseduo-card with front "anki-tags" (case sensitive) and back being a string of tags
in Anki format (each separate word becomes a tag), those tags are applied to all subsequent cards.
In the example above, every generated card would be tagged with "neuro peds tumors".


Media
-----
If you copy paste an image file INLINE (with text flowing around it) at the appropriate place in the bullet list, it will be imported to Anki and displayed. This feature is not extensively tested. Images are not currently exported from Anki.


Import
------
For whatever reason when you initially import, Anki is perfectly happy to try to import a Word document as a CVS file. To use this addon, you must change the file
type to (.docx) in the file picker dialog before selecting the file.

Allow HTML must be checked or else you'll get escaped HTML in your cards. For now leave model as Basic and Field mappings as default. I will clean up all these options later.

Export
------
Adds a export option "Cards as Word document". The front of the card becomes the top level indent and the back becomes the second level indent. If card front has the format "x: y: z", these levels become nested. Images are not exported.



Warning
-------
I have not yet extensively tested this. There are likely unancipated issues. It is working for me with my current version of Word (1902) on the latest OSX (as of 3/16/19) and Windows 10. 


TODO
----
- create a unique model for the cards and improve css styling
- word styling to html
- eventually option to sync word docs against collection (maybe....)
- support for odt (probably never)
