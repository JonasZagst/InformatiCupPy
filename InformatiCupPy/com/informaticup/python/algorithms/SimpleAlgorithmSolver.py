from InformatiCupPy.com.informaticup.python.algorithms.ISolver import ISolver
from InformatiCupPy.com.informaticup.python.algorithms.EasyDijkstraAlgorithm import EasyDijkstraAlgorithm as Dij
from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper
import sys
from _thread import start_new_thread
from threading import Thread
import pandas as pd


class SimpleAlgorithmSolver(ISolver):
    """ Simple algorithm to solve an input problem. ----- not completely implemented yet -----
        Works by looping through the passengers in the order of the their priority/target time.
        Uses dijkstra algorithm for shortest path problems. """

    def __init__(self, input_from_file):
        self.stations = input_from_file[0]
        self.lines = input_from_file[1]
        self.trains = input_from_file[2]
        self.passengers = input_from_file[3]
        self.time = 0
        self.df = self.generate_data_frame()

    def solve(self, input):
        """ Method to solve an input problem.
            :param input: input list (result of Input_Parser.parse_input())
        """
        # setting up the graph
        graph = Helper.set_up_graph(self.stations, self.lines)

        # list_threads = []

        # starting solving algorithm
        while self.check_break_condition():
            count = 0
            while self.check_inner_break_condition() and count <= 5:
                if self.get_free_trains():
                    chosen_passenger = self.choose_next_passenger()
                    if self.time == 0:
                        # do stuff for wildcard trains here
                        break
                    chosen_train = self.get_nearest_possible_train(passenger=chosen_passenger, graph=graph)
                    chosen_train_pos = self.df[chosen_train.id + "-position"].iloc[self.time]
                    chosen_passenger_pos = self.df[chosen_passenger.id + "-position"].iloc[self.time]
                    if chosen_passenger_pos == chosen_train_pos:
                        self.board_passenger(chosen_passenger, chosen_train)
                        # t = Thread(target=self.depart_train, args=(chosen_train, chosen_passenger, self.time, graph))
                        # list_threads.append(t)
                        # t.start()
                    else:
                        pass
                        # start_new_thread(self.bring_train_to_passenger, (chosen_train, chosen_passenger.position,
                        #                                                  self.time, graph,))
                    count += 1
            self.time += 1
            self.add_new_row(self.time)

            # for demo reasons:
            if self.time > 20:
                break

        # for thread in list_threads:
        # thread.join(timeout=20.0)

    def add_new_row(self, time):
        try:
            self.df.iloc[self.time]
        except IndexError:
            self.df = self.df.append(self.df.iloc[time - 1], ignore_index=True)

    def generate_data_frame(self):
        """
        Generates a pandas DataFrame with all object attributes that change over time.
        Columns: name = object.id + "-" + attribute (e.g.)
        Rows: only generates row 0 that contains the initial values of all objects
        :return: Returns the generated DataFrame with 1 row (index 0).
        """
        columns = []
        row_0 = []
        for station in self.stations:
            columns.append(station.id + "-current_capacity")
            row_0.append(station.current_capacity)

        for line in self.lines:
            columns.append(line.id + "-current_capacity")
            row_0.append(line.current_capacity)

        for train in self.trains:
            columns.append(train.id + "-current_capacity")
            columns.append(train.id + "-passengers")
            columns.append(train.id + "-position")
            columns.append(train.id + "-is_on_line")
            row_0.append(train.current_capacity)
            row_0.append("")  # no passengers in trains = empty string
            row_0.append(train.position)
            row_0.append(train.is_on_line)

        for passenger in self.passengers:
            columns.append(passenger.id + "-position")
            columns.append(passenger.id + "-is_in_train")
            row_0.append(passenger.position)
            row_0.append(passenger.is_in_train)

        df = pd.DataFrame(columns=columns, data=[row_0], index=[0])

        return df

    def depart_train(self, train, passenger, start_time, graph):
        length, stations, lines = Dij.calculate_shortest_path(graph, train.position, passenger.target_station)
        end_time = int(length / float(train.speed)) + start_time
        train.is_on_line = True
        while train.position != stations[1]:
            line = Helper.get_element_from_list_by_id(lines[0], self.lines)
            if line.current_capacity == 0 and not train.is_on_line:
                # delay train
                start_time += 1
                end_time += 1
            if self.time == start_time and not train.is_on_line:
                line.current_capacity -= 1
                train.is_on_line = True
                train.journey_history[self.time] = train.position
            if self.time == end_time:
                line.current_capacity += 1
                train.is_on_line = False
                train.position = stations[1]

    def bring_train_to_passenger(self, train, passenger_position, start_time, graph):
        length, stations, lines = \
            Dij.calculate_shortest_path(graph, train.position, passenger_position)
        end_time = int(length / float(train.speed)) + 1
        train.is_on_line = True
        while train.position != stations[1]:
            # check if train can travel first line:
            line = Helper.get_element_from_list_by_id(lines[0], self.lines)
            if line.current_capacity == 0:
                # delay train
                start_time += 1
                end_time += 1
            if self.time == start_time:
                line.current_capacity -= 1
                train.journey_history[self.time] = train.position
            if self.time == end_time:
                line.current_capacity += 1
                train.is_on_line = False
                train.position = stations[1]

    def board_passenger(self, passenger, train):
        """ Boards a passenger on a specific train. Adds boarding to the passengers journey_history and
            applies changes to the dataframe (not to the objects!).
            :param passenger: passenger that should be boarded.
            :param train: train on which the passenger should be boarded.
        """
        passenger.journey_history[self.time] = train.id
        self.df[train.id + "-current_capacity"].iloc[self.time] = \
            self.df[train.id + "-current_capacity"].iloc[self.time] - passenger.group_size
        self.df[train.id + "-passengers"].iloc[self.time] = \
            self.df[train.id + "-passengers"].iloc[self.time] + passenger.id + ";"
        self.df[passenger.id + "-is_in_train"] = True

    def check_inner_break_condition(self):  # has to be improved by debugging more advanced solutions of this algorithm
        for train in self.trains:
            for passenger in self.passengers:
                if self.df[train.id + "-current_capacity"].iloc[self.time] - int(passenger.group_size) >= 0 \
                        and not self.df[passenger.id + "-is_in_train"].iloc[self.time] \
                        and not self.df[train.id + "-is_on_line"].iloc[self.time]:
                    return True
        return False

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
                    and self.df[train.id + "-passengers"].iloc[self.time] == "":
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
        try:
            best_train = (possible_trains[0], sys.maxsize)  # tuple: (train, distance of train to passenger)
        except IndexError:
            return

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
        return best_train[0]

    def choose_next_passenger(self):
        """ Chooses the next passenger with should be brought to its target station.
            Chooses the passenger whose target_time is the lowest (only passengers that haven't reached their
            target station yet can be chosen).
            Returns the chosen passenger.
        """
        try:
            next_passenger = self.passengers[0]
        except IndexError:
            return
        for passenger in self.passengers:
            if int(passenger.target_time) < int(next_passenger.target_time) \
                    and passenger.target_station != self.df[passenger.id + "-position"].iloc[self.time] \
                    and not self.df[passenger.id + "is_in_train"].iloc[self.time]:
                next_passenger = passenger
        return next_passenger

    def get_name(self):
        return "simple-algorithm"

    def get_trains_and_passengers(self) -> list:
        return [self.trains, self.passengers]
