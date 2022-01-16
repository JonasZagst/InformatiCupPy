import random


class InputGenerator:

    def __init__(self):
        self.number_of_stations = 0
        self.number_of_trains = 0
        self.number_of_passengers = 0
        self.number_of_lines = 0
        self.station_max_cap = 0
        self.line_max_length = 0
        self.line_max_cap = 0
        self.train_max_max_speed = 0
        self.train_max_cap = 0
        self.passenger_max_group_size = 0
        self.file_name = ''
        self.number_of_files = 0
        self.station_cap_list = []

    def get_number_of_objects(self):
        """
        This method is used to get the number of objects, which should be ge generated
        """

        print('Wie viele Bahnhöfe soll die Inputdatei haben?')
        self.number_of_stations = int(input())
        print('Wie viele Strecken soll die Inputdatei haben?')
        self.number_of_lines = int(input())
        print('Wie viele Züge soll die Inputdatei haben?')
        self.number_of_trains = int(input())
        print('Wie viele Passagiere soll die Inputdatei haben?')
        self.number_of_passengers = int(input())

    def get_specifications(self):
        """
        This method is used to get the specification of the object attributes
        """

        print('Wie hoch soll die maximale Kapazität der Bahnhöfe sein?')
        self.station_max_cap = int(input())
        print('Wie lang soll eine Strecke maximal sein?')
        self.line_max_length = int(input())
        print('Wie hoch soll die maximale Kapazität der Strecken sein?')
        self.line_max_cap = int(input())
        print('Wie hoch soll die maximale Maximalgeschwindigkeit der Züge sein?')
        self.train_max_max_speed = int(input())
        print('Wie hoch soll die Maximale Kapazität der Züge sein?')
        self.train_max_cap = int(input())
        print('Wie groß soll eine Passagiergruppe maximal sein?')
        self.passenger_max_group_size = int(input())
        print('Wie soll die Inputdatei heißen?')
        self.file_name = str(input())
        print('Wie viele Files sollen generiert werden?')
        self.number_of_files = int(input())

    def generate_input_file(self):
        """
        This method is used to get the user specifications and to  generate all objects and write them into a file
        """

        self.get_number_of_objects()
        self.get_specifications()

        # generation of objects for each required file
        for i in range(1, self.number_of_files + 1):
            self.input_file = open(self.file_name + "_" + str(i) + ".txt", "w+")
            self.generate_stations()
            self.generate_lines()
            self.generate_trains()
            self.generate_passengers()
            self.input_file.close()

    def generate_stations(self):
        """
        This method is used to generate the station strings randomly but based on user specifications
        and write them into the input file
        """

        self.input_file.write("# Bahnhoefe: str(ID) int(Kapazitaet) \n")
        self.input_file.write("[Stations]\n")

        # generate a station based on user requirements  for each required station
        for x in range(1, self.number_of_stations + 1):
            station_string = "S" + str(x) + " " + str(random.randint(1, self.station_max_cap)) + " \n"
            self.station_cap_list.append(int(station_string[3:station_string.__len__()]))
            self.input_file.write(station_string)

    def generate_lines(self):
        """
        This method is used to generate the line strings randomly but based on user specifications
        and write them into the input file
        """

        line_list = []

        self.input_file.write("\n# Strecken: str(ID) str(Anfang) str(Ende) dec(Laenge) int(Kapazitaet)\n")
        self.input_file.write("[Lines]\n")

        # generate lines
        for x in range(self.number_of_lines):
            line_string = "L" + str(x) + " "

            line_beginning = random.randint(1, self.number_of_stations)
            line_ending = random.randint(1, self.number_of_stations)

            if line_beginning != line_ending:
                line_string = line_string + "S" + str(line_beginning) + " " + "S" + str(line_ending) + " "
            else:
                if line_beginning == self.number_of_stations - 1:
                    line_beginning = line_beginning - 1
                elif line_beginning == 0:
                    line_beginning = line_beginning + 1
                else:
                    line_beginning = line_beginning + 1
                line_string = line_string + "S" + str(line_beginning) + " " + "S" + str(line_ending) + " "

            line_string = line_string + str(random.randint(1, self.line_max_length)) + " " + str(
                random.randint(1, self.line_max_cap)) + "\n"
            line_list.append(line_string)

        all_lines = ""
        missing_station = []
        temporary_line_list = []

        # getting all stations now connected
        for i in line_list:
            all_lines = all_lines + i[4] + i[7]

        # getting all missing lines (station not connected)
        for i in range(1, self.number_of_stations + 1):
            if str(i) not in all_lines:
                missing_station.append(str(i))

        # appending all missing line strings (of not connected stations) to the line_list
        for i in missing_station:
            missing_line_string = "L" + str(self.number_of_lines + int(i)) + " " + "S" + str(i) + " " + "S" + str(
                random.randint(1, self.number_of_stations)) + " " + str(
                random.randint(1, self.line_max_length)) + " " + str(random.randint(1, self.line_max_cap)) + "\n"
            line_list.append(missing_line_string)

        # deletes duplicates
        line_list = list(dict.fromkeys(line_list))

        # getting other duplicates
        for i in line_list:
            a = i.replace("S" + str(i[7]) + " " + "S" + str(i[4]), "X")
            temporary_line_list.append(a)

        # deleting other duplicates
        line_list = temporary_line_list
        temporary_line_list2 = []
        for i in line_list:
            if not i.__contains__("X"):
                temporary_line_list2.append(i)
        line_list = temporary_line_list2

        # unify line IDs
        counter = 0
        temporary_line_list3 = []
        for i in line_list:
            counter = counter + 1
            index = i.find(" ")
            current_line_id = i[0:index]
            a = i.replace(current_line_id, "L" + str(counter))
            temporary_line_list3.append(a)
        line_list = temporary_line_list3

        # writing all lines into the input file
        for i in line_list:
            self.input_file.write(i)

    def generate_trains(self):
        """
        This method is used to generate the train strings randomly but based on user specifications
        and write them into the input file
        """
        self.input_file.write("\n# Zuege: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazitaet)\n")
        self.input_file.write("[Trains]\n")

        train_list = []

        # generate trains based on user requirements
        for x in range(1, self.number_of_trains + 1):
            first_station = random.randint(1, self.number_of_stations)

            if first_station != self.number_of_stations:
                train_string = "T" + str(x) + " " + "S" + str(first_station) + " " + str(
                    random.randint(1, self.train_max_max_speed - 1)) + " " + str(
                    random.randint(1, self.train_max_cap - 1)) + "\n"
            else:
                train_string = "T" + str(x) + " " + "*" + " " + str(
                    random.randint(1, self.train_max_max_speed - 1)) + " " + str(
                    random.randint(1, self.train_max_cap - 1)) + "\n"
            train_list.append(train_string)

        # checking capacity of first station
        for i in range(1, self.number_of_stations + 1):
            for a in train_list:
                counter = 0
                if a.__contains__("S" + str(i)):
                    counter = counter + 1
            if counter > self.station_cap_list[i - 1]:
                number_of_wrong_trains = counter - self.station_cap_list[i - 1]
                counter2 = 0
                for c in train_list:
                    if counter2 < number_of_wrong_trains:
                        if c.contains("S" + str(i)):
                            index_c = train_list.index(c)
                            new_string = c
                            train_list.remove(c)
                            counter2 = counter2 + 1
                            new_string = new_string.replace("S" + str(i), "*")
                            train_list.remove(c)
                            train_list.insert(index_c, new_string)

        for i in train_list:
            self.input_file.write(i)

    def generate_passengers(self):
        """
        This method is used to generate the passenger strings randomly but based on user specifications
        and write them into the input file
        """
        self.input_file.write(
            "\n# Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengroeße) int(Ankunftszeit)\n")
        self.input_file.write("[Passengers]\n")

        # generate passengers based on user requirements
        for x in range(1, self.number_of_passengers):
            passenger_string = "P" + str(x) + " "

            passenger_start = random.randint(1, self.number_of_stations-1)
            passenger_arrival = random.randint(1, self.number_of_stations-1)

            if passenger_start != passenger_arrival:
                passenger_string = passenger_string + "S" + str(passenger_start) + " " + "S" + str(
                    passenger_arrival) + " "
            else:
                if passenger_start == self.number_of_stations - 1:
                    passenger_start = passenger_start - 1
                elif passenger_start == 0:
                    passenger_start = passenger_start + 1
                else:
                    passenger_start = passenger_start + 1
                passenger_string = passenger_string + "S" + str(passenger_start) + " " + "S" + str(
                    passenger_arrival) + " "
            passenger_string = passenger_string + str(random.randint(1, self.passenger_max_group_size)) + " " + str(
                random.randint(1, self.number_of_passengers * 2)) + "\n"
            self.input_file.write(passenger_string)
