class Error(Exception):
    pass

class TooLong(Error):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class NotFound(Error):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message