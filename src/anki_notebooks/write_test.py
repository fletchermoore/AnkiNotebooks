

from write import writeDoc, createDocument

sampleContent = [
    (0, "this"),
    (1, "is"),
    (2, "my"),
    (3, "awesome"),
    (2, "document"),
    (1, "go home youre drunk")
]

writeDoc("sample.docx", sampleContent)
