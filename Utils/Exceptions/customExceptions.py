class CustomException(Exception):
    def __init__(self, statusCode, message):
        self.statusCode = statusCode
        self.message = message