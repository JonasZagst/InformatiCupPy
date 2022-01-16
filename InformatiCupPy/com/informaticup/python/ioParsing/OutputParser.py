import _thread
import sys
import threading
from contextlib import contextmanager

from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotSolveInput, TimeoutException, \
    CannotBoardPassenger
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.objects.Train import Train


class OutputParser:
    @staticmethod
    def parse_output_files(solvers: list, input):
        """Executes algorithms, takes the output and parses it into the output.txt file."""

        # TODO: catch CannotParseInputException
        # logging.error("Cannot read input file")

        # timeout for algorithms taking to long
        @contextmanager
        def time_limit(seconds, msg=''):
            timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
            timer.start()
            try:
                yield
            except KeyboardInterrupt:
                raise TimeoutException("Timed out for operation {}".format(msg))
            finally:
                # if the action ends in specified time, timer is canceled
                timer.cancel()

        best_delay_time = sys.maxsize

        # running through all algorithms
        for solver in solvers:
            output_str = ""

            try:
                with time_limit(600, 'sleep'):
                    delay_accumulated = solver.solve()

                    # performance rating of the distinct algorithms used
                    print(solver.get_name() + " - accumulated delay time: " + str(delay_accumulated))

                    for i in solver.get_trains_and_passengers()[0]:
                        if isinstance(i, Train):
                            output_str += i.to_output(input)

                    for i in solver.get_trains_and_passengers()[1]:
                        if isinstance(i, Passenger):
                            output_str += i.to_output(input)
            except CannotBoardPassenger:
                delay_accumulated = sys.maxsize
            except CannotSolveInput:
                delay_accumulated = sys.maxsize
            except TimeoutException:
                print(solver.get_name() + " --- execution timed out ----")
                output_str = "--- execution timed out ---- \n \n"
            except Exception:
                output_str = "--- an error occurred during execution of the algorithm ---- \n \n"

            if best_delay_time > delay_accumulated:
                best_delay_time = delay_accumulated
                output_file = open("InformatiCupPy/com/informaticup/input-output/output.txt", "w+")
                output_file.write(output_str)
                output_file.close()

            file = open("InformatiCupPy/com/informaticup/input-output/output-" + solver.get_name() + ".txt", "w+")
            file.write(output_str)
            file.close()

        if best_delay_time == sys.maxsize:
            output_file = open("InformatiCupPy/com/informaticup/input-output/output.txt", "w+")
            output_file.write("input file is not solvable")
            output_file.close()

        return output_str

    @staticmethod
    def parse_output_files_to_stdout(solvers: list, input):
        """Takes output from algorithms, parses it into the output.txt file and prints it to stdout."""

        sys.stdout = OutputParser.parse_output_files(solvers)
