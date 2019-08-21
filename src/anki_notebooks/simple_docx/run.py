class Run:
    def __init__(self, text, run_type="text"):
        # types are "test" or "image"
        self.type = run_type
        # content is the actual text or image rId
        self.text = text

    def print(self):
        print(self.type + ': ' + self.text)
