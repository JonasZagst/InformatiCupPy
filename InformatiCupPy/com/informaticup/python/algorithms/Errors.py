class CannotDepartTrain(Exception):
    def __init__(self, time):
        self.time = time


class CannotBoardPassenger(Exception):
    pass


class NoPassengerChosen(Exception):
    pass


class NoTrainChosen(Exception):
    pass


class CannotSolveInput(Exception):
    pass


class ProblemWithPassenger(Exception):
    pass


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

class CannotParseInputException(Exception):

    def print_message(self):
        print("Cannot read input file")
