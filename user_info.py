class user_info():
    id = ""
    email = ""
    displayname = ""
    nickname = ""
    avatar = ""

    def __init__(self, parent=None, *args, **kwargs):
        # self.signal = QtCore.SIGNAL("signal")
        self.Init(*args, **kwargs)
    def Init(self, id , email, displayname, nickname, avatar):
        self.id = id
        self.email = email
        self.displayname = displayname
        self.nickname = nickname
        self.avatar = avatar
