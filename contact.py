class contact:
    id = ""
    title = ""
    selected = ""
    type = ""

    def __init__(self, parent=None, *args, **kwargs):
        self.Init(*args, **kwargs)

    def Init(self, id, title, selected, type):
        self.id = id
        self.title = title
        self.selected = selected
        self.type = type
