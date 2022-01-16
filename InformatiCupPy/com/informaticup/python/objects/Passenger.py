from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper


class Passenger:
    """Class representation for passengers"""

    def __init__(self, original_id, original_initial_station, original_target_station, group_size, target_time):
        self.id = ""
        self.original_id = original_id
        self.initial_station = ""
        self.original_initial_station = original_initial_station
        self.target_station = ""
        self.original_target_station = original_target_station
        self.group_size = int(group_size)
        self.target_time = int(target_time)
        self.position = self.initial_station
        self.interim_target = None
        self.reached_interim_target = False
        self.is_in_train = False
        self.reached_target = False
        self.journey_history = {}

    def to_string(self):
        """Returns objects properties as String fitting the input format."""

        return "%s %s %s %s %s" % (self.id,
                                   self.initial_station,
                                   self.target_station,
                                   self.group_size,
                                   self.target_time)

    def to_output(self, input):
        """Returns objects properties as String fitting the output format."""

        output = "[Passenger:%s]" % self.original_id

        # check if dictionary is empty
        if not self.journey_history:
            return output + "\n\n"

        for key, value in self.journey_history.items():
            if value.startswith("T"):
                self.journey_history[key] = Helper.get_element_from_list_by_id(value, input[2]).original_id

        for key, value in self.journey_history.items():
            if value == "Detrain":
                output += "\n%s Detrain" % key
            else:
                output += "\n%s Board %s" % (str(key), value)

        return output + "\n\n"

    def set_internal_id(self, id):
        self.id = id

    def set_initial_station(self, internal_initial_station):
        self.initial_station = internal_initial_station
        self.position = self.initial_station

    def set_target_station(self, internal_target_station):
        self.target_station = internal_target_station

    def get_original_initial_station(self):
        return self.original_initial_station

    def get_original_target_station(self):
        return self.original_target_station
