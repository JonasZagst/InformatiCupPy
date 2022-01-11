from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.AdvancedDijkstraAlgorithm import AdvancedDijkstraAlgorithm as Dij
from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotDepartTrain, NoPassengerChosen, \
    NoTrainChosen, CannotBoardPassenger, CannotSolveInput, ProblemWithPassenger
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.objects.Train import Train
import sys
import pandas as pd
import math


class SimpleTrainParallelizationAlgorithm(ISolver):
    """ Simple algorithm to solve an input problem. The basic idea of this algorithm is to have multiple trains running
        at the same time (-> parallelization). Passengers are prioritized in terms of their target time.
        All attributes which can change over time (such as position, current capacity, ...) are stored in a dataframe.
        Every change in these attributes is also shown in the dataframe.
        The algorithm consists of a loop that will only break if all passengers have reached their targets. For each
        time step / round, as many trains as possible (up to a certain maximum) are started (= depart).
        Uses dijkstra algorithm for shortest path problems (e.g. to choose the nearest train or the shortest path to
        the target station).
    """

    # TODO:
    #       -fix bug with station capacity and recursion depth
    #       -add comments
    #       -parameter for wildcards
    #       -intelligent swap (board passengers before swap), parameter intelligent_swap=True/False
    #       -testing (different inputs)

    def __init__(self, input_from_file, parallelization_factor=1.0, set_wildcards=1.0):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
        self.time = 0
        self.df = self.generate_data_frame()
        self.max_parallelization_coefficient = min(len(self.stations), len(self.lines), len(self.passengers))
        self.parallelization_factor = parallelization_factor
        self.graph = Helper.set_up_graph(self.stations, self.lines)
        self.set_wildcards = set_wildcards
        self.path_dict = Helper.set_up_path_dict(self.stations)

    def solve(self):
        """ Solves the input problem. Includes the main loop
            of the algorithm (more details in class description).
            :returns: total delay time.
        """
        # starting solving algorithm/loop
        while self.check_break_condition():
            #print(self.time)
            inner_loop_index = 0  # set counter for inner loop = 0
            while self.check_inner_break_condition() and inner_loop_index <= \
                    max(1.0, self.max_parallelization_coefficient * self.parallelization_factor):

                if self.time == 0:
                    self.set_wildcard_trains()  # if time = 0, wildcard trains will be set
                    break

                if self.get_free_trains():  # if free trains left
                    try:
                        chosen_passenger = self.choose_next_passenger()  # choose next passenger by target time
                        if self.df[chosen_passenger.id + "-is_in_train"].iloc[self.time]:
                            chosen_train = Helper.get_element_from_list_by_id(
                                self.df[chosen_passenger.id + "-position"].iloc[self.time], self.trains)
                            if self.df[chosen_train.id + "-is_on_line"].iloc[self.time]:
                                self.df[chosen_passenger.id + "-checked"].iloc[self.time] = True
                                continue
                        else:
                            # choose nearest train
                            chosen_train = self.get_nearest_possible_train(passenger=chosen_passenger)
                    except NoPassengerChosen:
                        break
                    except NoTrainChosen:
                        break

                    # get current positions of chosen train and passenger
                    chosen_train_pos = self.df[chosen_train.id + "-position"].iloc[self.time]
                    chosen_passenger_pos = self.df[chosen_passenger.id + "-position"].iloc[self.time]

                    # boarding, departing and detraining:
                    if chosen_passenger_pos == chosen_train_pos:  # if train and passenger on same station
                        try:
                            # depart train after boarding
                            end_time = \
                                self.depart_train(chosen_train, chosen_passenger.target_station, self.time + 1)
                            self.board_passenger(chosen_passenger, chosen_train)  # board passenger on train
                            # detrain passenger after arriving at target station
                            self.detrain_passenger(chosen_passenger, chosen_train, end_time)
                        except CannotDepartTrain as e:  # if train cannot depart: detrain passenger again
                            # self.detrain_passenger(chosen_passenger, chosen_train, e.time + 1)
                            pass
                        except CannotBoardPassenger:
                            pass
                    elif self.df[chosen_passenger.id + "-is_in_train"].iloc[self.time]:
                        try:
                            end_time = self.depart_train(chosen_train, chosen_passenger.target_station, self.time)
                            self.detrain_passenger(chosen_passenger, chosen_train, end_time)

                        except CannotDepartTrain:
                            pass
                    else:  # if passenger and train are not at the same station
                        try:
                            # bring train to passenger
                            self.depart_train(chosen_train, chosen_passenger_pos, self.time)
                        except CannotDepartTrain:
                            pass

                    inner_loop_index += 1

                else:
                    break  # break inner loop if no free train available -> go on to next time step

            self.time += 1  # go to next time step
            self.add_new_row(self.time)  # add row (if needed) for new time step
            self.df.to_csv("InformatiCupPy/com/informaticup/python/algorithms/df.csv")

        # calculate total delay of the timetable
        delay = 0
        for passenger in self.passengers:
            # search the point of time the passenger reached its target station
            for i in range(len(self.df)):
                pos = self.df[passenger.id + "-position"].iloc[i]
                if passenger.target_station == pos:
                    passenger_delay = i - passenger.target_time
                    if passenger_delay > 0:  # if passenger is late
                        delay += passenger_delay  # add delay time to total delay
                    break

        return delay

    def add_new_row(self, time):
        """ Adds a new row for at index=time to the dataframe (self.df). If the row with this index does already exist,
            this method does nothing.
            :param time: time for which the row should be added (equals index of the new row).
        """
        try:
            self.df.iloc[time]
        except IndexError:  # if row does not exist, create a new one:
            self.df = self.df.append(self.df.iloc[time - 1], ignore_index=True)  # new row is copy of the previous
            for column in self.df.filter(regex="^T\\d+-status$"):  # status of every train is set to an empty string
                self.df[column].iloc[time] = ""
            for column in self.df.filter(regex="^T\\d+-checked$|^P\\d+-checked$"):  # every 'checked' is set to false
                self.df[column].iloc[time] = False

    def board_passenger(self, passenger, train):
        """ Boards a passenger on a specific train. Adds boarding to the passengers journey_history and
            applies changes to the dataframe (not to the objects!).
            :param passenger: passenger that should be boarded.
            :param train: train on which the passenger should be boarded.
        """

        if self.df[train.id + "-status"].iloc[self.time] != "":
            raise CannotBoardPassenger()  # cannot board passenger if train is currently boarding/detraining/departing

        # adds boarding to journey history (and therefore to the output)
        passenger.journey_history[self.time] = train.id

        # apply changes in attributes caused by boarding the passenger to the dataframe
        self.df[train.id + "-status"].iloc[self.time] = "boarded"

        # update attributes from current point of time to the end of the dataframe
        for i in range(self.time, len(self.df)):
            self.df[train.id + "-current_capacity"].iloc[i] = \
                self.df[train.id + "-current_capacity"].iloc[i] - passenger.group_size  # reduce train capacity
            # write passenger into the train's passengers attribute
            self.df[train.id + "-passengers"].iloc[i] = self.df[train.id + "-passengers"].iloc[i] + passenger.id + ";"
            self.df[passenger.id + "-is_in_train"].iloc[i] = True  # set passenger is_in_train True
            self.df[passenger.id + "-position"].iloc[i] = train.id  # set passenger's position to train id

    def check_break_condition(self):
        """ Checks if the main loop of the algorithm can finish/stop. Works with the dataframe.
            :return True, as long as there are still passengers who haven't reached their target station yet.
            :return False, if all passengers have already reached their target station.
        """
        for passenger in self.passengers:
            position = self.df[passenger.id + "-position"].iloc[self.time]
            if passenger.target_station != position:
                return True
        return False

    def check_inner_break_condition(self):
        """ Checks if the condition for the inner while-loop in the solve()-method is fulfilled.
            As long as the inner condition is fulfilled, the algorithm tries to start new trains in the same
            round (/point of time). The algorithm stops starting new trains (according to this method) if all free
            trains do not have enough capacity for any free passenger and/or possible trains have already been checked
            (algorithm has tried to start them).
            :returns: True, if condition is fulfilled.
                      False, if condition is not fulfilled.
        """
        for train in self.trains:
            for passenger in self.passengers:
                if self.df[train.id + "-current_capacity"].iloc[self.time] - int(passenger.group_size) >= 0 \
                        and not self.df[passenger.id + "-is_in_train"].iloc[self.time] \
                        and not self.df[train.id + "-is_on_line"].iloc[self.time] \
                        and not self.df[train.id + "-checked"].iloc[self.time]:
                    return True
        return False

    def choose_next_passenger(self):
        """ Chooses the next passenger with should be brought to its target station.
            Chooses the passenger whose target_time is the lowest (only passengers that haven't reached their
            target station yet can be chosen).
            Returns the chosen passenger.
        """
        dummy_passenger = Passenger("", "", "", 0, sys.maxsize)  # create a dummy passenger with maximum target time
        next_passenger = dummy_passenger

        for passenger in self.passengers:
            if int(passenger.target_time) < int(next_passenger.target_time) \
                    and not self.df[passenger.id + "-checked"].iloc[self.time]\
                    and not passenger.reached_target:
                next_passenger = passenger
        if next_passenger != dummy_passenger:
            return next_passenger
        else:
            raise NoPassengerChosen()  # if dummy passenger is still the chosen passenger, no passenger could be chosen

    def depart_train(self, train, target, start_time):
        """ Departs a train at a certain time from its origin to a target station (no direct connection needed).
            Uses dijkstra-shortest-path-calculation to find the shortest way to the target station. Also performs a
            swap if needed (if no capacity at target station, a train at the target station departs just before the new
            train arrives. Adds the respective 'depart'-actions to the train's journey history (and therefore to the
            output) and performs the changes of passenger-, train-, station- and line-attributes on the dataframe
            (self.df).
            :param train: train which should be departed.
            :param target: target station (id).
            :param start_time: time when the train should be departed.
            :raise CannotDepartTrain: if train cannot depart (because a passenger is currently being boarded/detrained).
            :returns: end time / time of arrival at target station.
            """
        self.df[train.id + "-checked"].iloc[self.time] = True
        self.add_new_row(start_time)

        # if a passenger is currently being boarded/detrained, the train cannot depart
        if self.df[train.id + "-status"].iloc[start_time] != "" or self.df[train.id + "-position"].iloc[self.time] == target:
            raise CannotDepartTrain(start_time)

        # calculate total length of the shortest path to the target and determine stations and lines on the path
        length, stations, lines, self.path_dict = \
            Dij.calculate_shortest_path(self.graph,
                                        self.df[train.id + "-position"].iloc[start_time],
                                        target,
                                        self.path_dict)

        # depart on each line of the shortest path, begin departing at end time of the previous
        start_time_line = start_time
        for c in range(len(lines)):
            # get line-object from id
            line = Helper.get_element_from_list_by_id(lines[c], self.lines)
            # calculate arrival time at next station
            end_time_line = int(math.ceil(line.length / train.speed)) + start_time_line

            # check if the line is free / has enough capacity left for a new train
            can_depart = True
            for i in range(start_time_line, end_time_line):
                self.add_new_row(i)
                if self.df[line.id + "-current_capacity"].iloc[i] < 1:
                    can_depart = False

            can_swap = True
            self.add_new_row(end_time_line)
            if self.df[stations[c + 1] + "-current_capacity"].iloc[end_time_line] < 1:
                can_swap = False
                # try if swap is possible
                for swap_train in self.trains:
                    if self.df[swap_train.id + "-position"].iloc[end_time_line] == stations[c + 1] \
                            and self.df[swap_train.id + "-position"].iloc[end_time_line - 1] == stations[c + 1] \
                            and self.df[swap_train.id + "-status"].iloc[end_time_line - 1] == "" \
                            and self.df[swap_train.id + "-status"].iloc[end_time_line] == ""\
                            and not can_swap:
                        can_swap = True
                        swap_end = int(math.ceil(length / swap_train.speed)) + end_time_line - 1
                        for i in range(end_time_line - 1, swap_end):
                            self.add_new_row(i)
                            if self.df[line.id + "-current_capacity"].iloc[i] < 1:
                                can_depart = False
                                break
                        self.add_new_row(swap_end)
                        if self.df[stations[c] + "-current_capacity"].iloc[swap_end] < 0:
                            can_depart = False

            # if line is free, depart train, else raise CannotDepartTrain-Exception
            if not can_depart or not can_swap:
                if "L" in self.df[train.id + "-position"].iloc[start_time_line]:  #
                    self.df[train.id + "-position"].iloc[start_time_line] = stations[c]
                    self.df[train.id + "-is_on_line"].iloc[start_time_line] = False
                    self.df[stations[c] + "-current_capacity"].iloc[start_time_line] = \
                        self.df[stations[c] + "-current_capacity"].iloc[start_time_line] - 1
                raise CannotDepartTrain(start_time_line)  # if line is not free / has not enough capacity for the train

            train.journey_history[start_time_line] = line.id  # add departing to output
            self.df[train.id + "-status"].iloc[start_time_line] = "departed"  # change train status

            # loop through all time steps between start and end time and update dataframe
            for i in range(start_time_line, end_time_line):
                self.df[train.id + "-is_on_line"].iloc[i] = True
                self.df[line.id + "-current_capacity"].iloc[i] = self.df[line.id + "-current_capacity"].iloc[i] - 1
                self.df[train.id + "-position"].iloc[i] = line.id

            # increase station capacity after the train departs
            for i in range(start_time_line, len(self.df)):
                self.df[stations[c] + "-current_capacity"].iloc[i] = \
                    self.df[stations[c] + "-current_capacity"].iloc[i] + 1

            self.df[line.id + "-current_capacity"].iloc[end_time_line - 1] = \
                self.df[line.id + "-current_capacity"].iloc[end_time_line - 1] + 1

            self.add_new_row(end_time_line)

            # set target station as train position after train arrives and decrease its capacity
            for i in range(end_time_line, len(self.df)):
                self.df[train.id + "-position"].iloc[i] = stations[c + 1]
                self.df[stations[c + 1] + "-current_capacity"].iloc[i] = \
                    self.df[stations[c + 1] + "-current_capacity"].iloc[i] - 1

            # check if target station has enough capacity for train
            # if not enough capacity: depart a train at the station just before the other train arrives ("swap")
            if self.df[stations[c + 1] + "-current_capacity"].iloc[end_time_line] < 0:
                for swap_train in self.trains:
                    if self.df[swap_train.id + "-position"].iloc[end_time_line] == stations[c + 1] \
                            and swap_train.id != train.id \
                            and self.df[swap_train.id + "-position"].iloc[end_time_line - 1] == stations[c + 1]:
                        self.depart_train(swap_train, stations[c], end_time_line - 1)
                        break

            start_time_line = end_time_line  # start time of the next line is end time of the previous

            # if the train has reached its final target, set its is_on_line attribute to false
            if self.df[train.id + "-position"].iloc[end_time_line] == target:
                for i in range(end_time_line, len(self.df)):
                    self.df[train.id + "-is_on_line"].iloc[i] = False

        return end_time_line  # return the end time

    def detrain_passenger(self, passenger, train, time):
        """ Detrains a passenger from a train at a certain round / point of time.
            Adds 'Detrain' to the passengers journey history (and therefore to the output, later).
            Sets all attributes that are affected by detrain-action to the respective values in self.df."""
        self.add_new_row(time)
        if self.df[train.id + "-status"].iloc[time] != "":
            time += 1
            self.add_new_row(time)
        passenger.journey_history[time] = "Detrain"
        self.df[train.id + "-status"].iloc[time] = "detrained"
        self.df[passenger.id + "-checked"].iloc[time] = True
        for i in range(time, len(self.df)):
            self.df[train.id + "-passengers"].iloc[i] = \
                self.df[train.id + "-passengers"].iloc[i].replace(passenger.id + ";", "")
            self.df[passenger.id + "-is_in_train"].iloc[i] = False
            self.df[passenger.id + "-position"].iloc[i] = self.df[train.id + "-position"].iloc[i]
            self.df[train.id + "-current_capacity"].iloc[i] = \
                self.df[train.id + "-current_capacity"].iloc[i] + passenger.group_size
        if self.df[passenger.id + "-position"].iloc[time] == passenger.target_station:
            passenger.reached_target = True

    def generate_data_frame(self):
        """
        Generates a pandas DataFrame with all object attributes that change over time.
        Columns: name = object.id + "-" + attribute (e.g.)
        Rows: only generates row 0 that contains the initial values of all objects
        :return: Returns the generated DataFrame with 1 row (index 0).
        """
        columns = []
        row_0 = []

        trains_per_station = {}
        for train in self.trains:
            if train.position in trains_per_station.keys():
                trains_per_station[train.position] += 1
            else:
                trains_per_station[train.position] = 1

        for station in self.stations:
            columns.append(station.id + "-current_capacity")
            try:
                trains_at_station = trains_per_station[station.id]
            except KeyError:
                trains_at_station = 0
            row_0.append(station.capacity - trains_at_station)

        for line in self.lines:
            columns.append(line.id + "-current_capacity")
            row_0.append(line.capacity)

        for train in self.trains:
            columns.append(train.id + "-current_capacity")
            columns.append(train.id + "-passengers")
            columns.append(train.id + "-position")
            columns.append(train.id + "-is_on_line")
            columns.append(train.id + "-checked")  # boolean: true if algorithm already tried to depart that train
            columns.append(train.id + "-status")  # str: boarded/departed/detrained, to avoid 2 actions at the same time
            row_0.append(train.capacity)
            row_0.append("")  # no passengers in trains = empty string
            row_0.append(train.position)
            row_0.append(False)
            row_0.append(False)
            row_0.append("")

        for passenger in self.passengers:
            columns.append(passenger.id + "-position")
            columns.append(passenger.id + "-is_in_train")
            columns.append(passenger.id + "-checked")
            row_0.append(passenger.position)
            row_0.append(passenger.is_in_train)
            row_0.append(False)

        df = pd.DataFrame(columns=columns, data=[row_0], index=[0])

        return df

    def get_free_trains(self, passenger=None):
        """ Checks if there are free trains (trains that have enough capacity left for a specific group of passengers)
            and returns them.
            :param passenger: optional parameter, passenger that should fit into the train.
            :return: a list of all trains that fulfill the condition (empty list if no train fulfills condition).
        """
        possible_trains = []
        group_size = 0 if passenger is None else passenger.group_size
        for train in self.trains:
            if self.df[train.id + "-current_capacity"].iloc[self.time] - int(group_size) >= 0 \
                    and self.df[train.id + "-passengers"].iloc[self.time] == "" \
                    and not self.df[train.id + "-is_on_line"].iloc[self.time] \
                    and not self.df[train.id + "-checked"].iloc[self.time] \
                    and self.df[train.id + "-position"].iloc[self.time] != "*":
                possible_trains.append(train)
        return possible_trains

    def get_nearest_possible_train(self, passenger=None):
        """ Gets the nearest train that can take the passenger (by means of group size).
            Uses dijkstra shortest-path-calculation to identify the nearest train.
            :param passenger: passenger that shall use the train (needed for size check and path calculation).
            :return: nearest train.
        """

        possible_trains = self.get_free_trains(passenger=passenger)
        dummy_train = Train("", "", 0, 0)
        best_train = (dummy_train, sys.maxsize)  # tuple: (train, distance of train to passenger)

        for train in possible_trains:
            train_pos = self.df[train.id + "-position"].iloc[self.time]
            passenger_pos = self.df[passenger.id + "-position"].iloc[self.time]
            if train_pos == passenger_pos:
                # if there is a train that has already the same position as the passenger, return this train
                return train
            # else calculate shortest path:
            distance_to_passenger, _, __, self.path_dict = \
                Dij.calculate_shortest_path(self.graph, train_pos, passenger_pos, self.path_dict)
            # and return nearest train:
            if distance_to_passenger < best_train[1]:
                best_train = (train, distance_to_passenger)
        if best_train[0] != dummy_train:
            return best_train[0]
        else:
            raise NoTrainChosen

    def set_wildcard_trains(self):
        """ Sets wildcard trains. All wildcard trains will be set. First, it loops through the passengers and sets a
            wildcard train to all stations with passenger but without train. After that, the remaining wildcard trains
            are distributed on the stations with enough capacity left."""
        wildcard_trains = []
        for train in self.trains:
            if train.position == "*":
                wildcard_trains.append(train)

        if not wildcard_trains:
            return
        else:
            wildcard_trains.sort(key=lambda t: t.capacity, reverse=True)

        wildcards_to_set = int(self.set_wildcards * len(wildcard_trains))
        set_wildcards_until = len(wildcard_trains) - wildcards_to_set

        if len(wildcard_trains) == len(self.trains):
            for station in self.stations:
                if station.capacity > self.df[station.id + "-current_capacity"].iloc[self.time]:
                    self.df[wildcard_trains[0].id + "-position"] = station.id
                    self.df[station.id + "-current_capacity"].iloc[self.time] = \
                        self.df[station.id + "-current_capacity"].iloc[self.time] - 1
                    wildcard_trains[0].initial_position = station.id
                    wildcard_trains.pop(0)
                    break

        for passenger in self.passengers:
            pos = self.df[passenger.id + "-position"].iloc[self.time]
            station = Helper.get_element_from_list_by_id(pos, self.stations)
            if station.capacity == self.df[pos + "-current_capacity"].iloc[self.time]:
                self.df[wildcard_trains[0].id + "-position"] = pos
                self.df[pos + "-current_capacity"].iloc[self.time] = \
                    self.df[pos + "-current_capacity"].iloc[self.time] - 1
                wildcard_trains[0].initial_position = pos
                wildcard_trains.pop(0)
                if not wildcard_trains or len(wildcard_trains) <= set_wildcards_until:
                    return

        for station in self.stations:
            if station.capacity > self.df[station.id + "-current_capacity"].iloc[self.time]:
                self.df[wildcard_trains[0].id + "-position"] = station.id
                self.df[station.id + "-current_capacity"].iloc[self.time] = \
                    self.df[station.id + "-current_capacity"].iloc[self.time] - 1
                wildcard_trains[0].initial_position = station.id
                wildcard_trains.pop(0)
                if not wildcard_trains or len(wildcard_trains) <= set_wildcards_until:
                    return

        raise CannotSolveInput()  # Cannot solve input: too many wildcard trains for station capacities

    def get_name(self):
        return f"simple-train-parallelization-algorithm-{str(self.parallelization_factor)}-{str(self.set_wildcards)}"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
