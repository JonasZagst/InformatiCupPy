from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm as Dij
from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
from InformatiCupPy.com.informaticup.python.algorithms.Errors import CannotDepartTrain, NoPassengerChosen, \
    NoTrainChosen, CannotBoardPassenger
from InformatiCupPy.com.informaticup.python.objects.Passenger import Passenger
from InformatiCupPy.com.informaticup.python.objects.Train import Train
import sys
import pandas as pd


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
    #       -add wildcards
    #       -kommentieren und dokumentieren
    #       -intelligenter Swap (bei Swap gleich Passagiere mitnehmen)
    #       -für verschiedene Inputs testen und anpassen
    #       -finalen Dataframe plotten und evtl. zusammenhänge/optimierungsideen finden

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
        self.time = 0
        self.df = self.generate_data_frame()
        self.max_parallelization_coefficient = min(len(self.stations), len(self.lines), len(self.passengers))

    def solve(self):
        """ Solves the input problem. Includes the graph set-up (needed for dijkstra) and the main loop
            of the algorithm (more details in class description). Calculates, moreover, the delay time of the solution.
            :returns: delay time.
        """
        # setting up the graph
        graph = Helper.set_up_graph(self.stations, self.lines)

        # starting solving algorithm/loop
        while self.check_break_condition():
            print(self.time)
            inner_loop_index = 0
            self.set_checked_false()
            while self.check_inner_break_condition() and inner_loop_index <= self.max_parallelization_coefficient:
                if self.get_free_trains():
                    try:
                        chosen_passenger = self.choose_next_passenger()
                    except NoPassengerChosen:
                        break
                    if self.time == 0:
                        # do stuff for wildcard trains here
                        break
                    try:
                        chosen_train = self.get_nearest_possible_train(passenger=chosen_passenger, graph=graph)
                    except NoTrainChosen:
                        break
                    chosen_train_pos = self.df[chosen_train.id + "-position"].iloc[self.time]
                    chosen_passenger_pos = self.df[chosen_passenger.id + "-position"].iloc[self.time]
                    if chosen_passenger_pos == chosen_train_pos:
                        try:
                            end_time = \
                                self.depart_train(chosen_train, chosen_passenger.target_station, self.time + 1, graph)
                            self.board_passenger(chosen_passenger, chosen_train)
                            self.detrain_passenger(chosen_passenger, chosen_train, end_time)
                        except CannotDepartTrain:
                            pass
                        except CannotBoardPassenger:
                            pass
                    else:
                        try:
                            self.depart_train(chosen_train, chosen_passenger_pos, self.time, graph)
                        except CannotDepartTrain:
                            pass
                    inner_loop_index += 1
            self.time += 1
            self.add_new_row(self.time)

        # self.df.to_csv("algorithms\\df.csv")
        delay = 0
        for passenger in self.passengers:
            for i in range(len(self.df)):
                pos = self.df[passenger.id + "-position"].iloc[i]
                if passenger.target_station == pos:
                    passenger_delay = i - passenger.target_time
                    if passenger_delay > 0:
                        delay += passenger_delay
        return delay

    def add_new_row(self, time):
        try:
            self.df.iloc[time]
        except IndexError:
            self.df = self.df.append(self.df.iloc[time - 1], ignore_index=True)

    def board_passenger(self, passenger, train):
        """ Boards a passenger on a specific train. Adds boarding to the passengers journey_history and
            applies changes to the dataframe (not to the objects!).
            :param passenger: passenger that should be boarded.
            :param train: train on which the passenger should be boarded.
        """
        passenger.journey_history[self.time] = train.id
        for i in range(self.time, len(self.df)):
            self.df[train.id + "-current_capacity"].iloc[i] = \
                self.df[train.id + "-current_capacity"].iloc[i] - passenger.group_size
            self.df[train.id + "-passengers"].iloc[i] = self.df[train.id + "-passengers"].iloc[i] + passenger.id + ";"
            self.df[passenger.id + "-is_in_train"].iloc[i] = True
            self.df[passenger.id + "-position"].iloc[i] = train.id

    def check_break_condition(self):
        """ Checks if the main loop of the algorithm can finish/stop. Works with the dataframe.
            :return True, as long as there are still passengers who haven't reached their target station yet.
            :return False, if all passengers have already reached their target station.
        """
        df_positions = self.df.filter(regex="^P\\d+-position$")
        for passenger in self.passengers:
            position = df_positions[passenger.id + "-position"].iloc[self.time]
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
        dummy_passenger = Passenger("", "", "", 0, sys.maxsize)
        next_passenger = dummy_passenger

        for passenger in self.passengers:
            if int(passenger.target_time) < int(next_passenger.target_time) \
                    and passenger.target_station != self.df[passenger.id + "-position"].iloc[self.time] \
                    and not self.df[passenger.id + "-is_in_train"].iloc[self.time]:
                next_passenger = passenger
        if next_passenger != dummy_passenger:
            return next_passenger
        else:
            raise NoPassengerChosen()

    def depart_train(self, train, target, start_time, graph):
        self.df[train.id + "-checked"].iloc[self.time] = True
        try:
            length, stations, lines = \
                Dij.calculate_shortest_path(graph, self.df[train.id + "-position"].iloc[start_time], target)
        except IndexError:
            length, stations, lines = \
                Dij.calculate_shortest_path(graph, self.df[train.id + "-position"].iloc[start_time-1], target)
        end_time = int(length / train.speed) + start_time
        start_time_line = start_time
        for c in range(len(lines)):
            line = Helper.get_element_from_list_by_id(lines[c], self.lines)
            end_time_line = int(line.length / train.speed) + start_time_line
            can_depart = True
            for i in range(start_time_line, end_time_line):
                self.add_new_row(i)
                if self.df[line.id + "-current_capacity"].iloc[i] < 1:
                    can_depart = False
                    break
            if can_depart:
                train.journey_history[start_time_line] = line.id
                for i in range(start_time_line, end_time_line):
                    self.df[stations[c] + "-current_capacity"].iloc[i] = \
                        self.df[stations[c] + "-current_capacity"].iloc[i] + 1
                    self.df[train.id + "-is_on_line"].iloc[i] = True
                    self.df[line.id + "-current_capacity"].iloc[i] = self.df[line.id + "-current_capacity"].iloc[i] - 1
                    self.df[train.id + "-position"].iloc[i] = line.id
                self.df[line.id + "-current_capacity"].iloc[end_time_line - 1] = \
                    self.df[line.id + "-current_capacity"].iloc[end_time_line - 1] + 1
                self.add_new_row(end_time_line)
                if self.df[stations[c + 1] + "-current_capacity"].iloc[end_time_line] < 1:  # swap
                    for swap_train in self.trains:
                        if self.df[swap_train.id + "-position"].iloc[end_time_line] == stations[c + 1]:
                            self.depart_train(swap_train, stations[c], end_time_line - 1, graph)
                            break
            else:
                raise CannotDepartTrain()

            self.df[train.id + "-position"].iloc[end_time_line] = stations[c + 1]

            start_time_line = end_time_line

            if self.df[train.id + "-position"].iloc[end_time_line] == target:
                self.df[train.id + "-is_on_line"].iloc[end_time_line] = False

        return end_time

    def detrain_passenger(self, passenger, train, time):
        """ Detrains a passenger from a train at a certain round / point of time.
            Adds 'Detrain' to the passengers journey history (and therefore to the output, later).
            Sets all attributes that are affected by detrain-action to the respective values in self.df."""
        self.add_new_row(time)
        passenger.journey_history[time] = "Detrain"
        self.df[train.id + "-passengers"].iloc[time] = \
            self.df[train.id + "-passengers"].iloc[time].replace(passenger.id + ";", "")
        self.df[passenger.id + "-is_in_train"].iloc[time] = False
        self.df[passenger.id + "-position"].iloc[time] = self.df[train.id + "-position"].iloc[time]
        self.df[train.id + "-current_capacity"].iloc[time] = \
            self.df[train.id + "-current_capacity"].iloc[time] + passenger.group_size

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
            row_0.append(station.current_capacity - trains_at_station)

        for line in self.lines:
            columns.append(line.id + "-current_capacity")
            row_0.append(line.current_capacity)

        for train in self.trains:
            columns.append(train.id + "-current_capacity")
            columns.append(train.id + "-passengers")
            columns.append(train.id + "-position")
            columns.append(train.id + "-is_on_line")
            columns.append(train.id + "-checked")  # boolean: true if algorithm already tried to depart that train
            row_0.append(train.current_capacity)
            row_0.append("")  # no passengers in trains = empty string
            row_0.append(train.position)
            row_0.append(train.is_on_line)
            row_0.append(False)

        for passenger in self.passengers:
            columns.append(passenger.id + "-position")
            columns.append(passenger.id + "-is_in_train")
            row_0.append(passenger.position)
            row_0.append(passenger.is_in_train)

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
                    and self.df[train.id + "-passengers"].iloc[self.time] == ""\
                    and not self.df[train.id + "-is_on_line"].iloc[self.time]:
                possible_trains.append(train)
        return possible_trains

    def get_nearest_possible_train(self, passenger=None, graph=None):
        """ Gets the nearest train that can take the passenger (by means of group size).
            Uses dijkstra shortest-path-calculation to identify the nearest train.
            :param passenger: passenger that shall use the train (needed for size check and path calculation).
            :param graph: Graph object of the input map.
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
            distance_to_passenger, _, __ = Dij.calculate_shortest_path(graph, train_pos, passenger_pos)
            # and return nearest train:
            if distance_to_passenger < best_train[1]:
                best_train = (train, distance_to_passenger)
        if best_train[0] != dummy_train:
            return best_train[0]
        else:
            raise NoTrainChosen

    def set_checked_false(self):
        """ Sets the attribute 'checked' to false for all trains (in self.df) at the current point of time."""
        for column in self.df.filter(regex="^T\\d+-checked$"):
            self.df[column].iloc[self.time] = False

    def get_name(self):
        return "simple-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]