class CannotDepartTrain(Exception):
    pass


class CannotBoardPassenger(Exception):
    pass


class NoPassengerChosen(Exception):
    pass


class NoTrainChosen(Exception):
    pass


class CannotSolveInput(Exception):
    pass


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg
