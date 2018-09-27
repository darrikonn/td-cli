class TodoException(Exception):
    def __init__(self, message, details=None, type="Error"):
        self.message = message
        self.details = details or message
        self.type = type

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
