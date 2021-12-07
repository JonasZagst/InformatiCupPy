from abc import abstractmethod


class ISolver:
    """ Interface for a solving algorithm. Each algorithm should implement this interface. """

    @abstractmethod
    def solve(self, input: list):
        """ Solves the input problem with some kind of algorithm and returns the solution as string. The single
            steps of the algorithm can be performed in different functions (if needed), but the final act of solving
            should happen within this function.
            --input: list of input objects, usually the result of the parse_input()-function of the InputParser.
            returns: solution of the input problem as correctly formatted string (according to the conventions
                     in the original task from GI)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """ Returns the name of the solving algorithm."""
        pass

    @abstractmethod
    def get_trains_and_passengers(self) -> list:
        """Returns the instances of trains and passengers for the output."""
        pass
