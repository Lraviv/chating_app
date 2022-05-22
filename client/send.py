'''
this handles data that meant to be
sent to server'''

class send(object):
    def __init__(self, function,msg):
        self.msg = msg
        self.func = function
        self.data = ""
        self.protocol()

    def protocol(self):
        # puts data in protocol structure
        self.data = str(self.msg), "|", str(self.function)
        print("sends to server:", self.data)
