class MainClassExp(Exception):
    def __init__(self, message):
        self.message = message


class ResultLong(MainClassExp):

    def __init__(self, message):
        super().__init__(message)


class InvalidSymbol(MainClassExp):

    def __init__(self, message):
        super().__init__(message)


class GameEnd(MainClassExp):

    def __init__(self, message):
        super().__init__(message)
