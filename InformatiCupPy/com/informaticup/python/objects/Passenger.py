class Passenger:

    def __init__(self, id, initial_station, target_station, group_size, target_time):
        # id of the passenger
        self.id = id
        # start station of this passenger
        self.initial_station = initial_station
        # target station of this passenger
        self.target_station = target_station
        # this is the number of persons eventually traveling with this passenger
        self.group_size = int(group_size)
        # the target time of arrival
        self.target_time = int(target_time)
        # the current position of the passenger
        self.position = initial_station
        # true if passenger currently in a train, else false
        self.is_in_train = False
        self.reached_target = False
        self.journey_history = {}

    """Returns objects properties as String fitting the input format."""

    def to_string(self):
        return "%s %s %s %s %s" % (self.id,
                                   self.initial_station,
                                   self.target_station,
                                   self.group_size,
                                   self.target_time)

    """Returns objects properties as String fitting the output format."""

    def to_output(self):
        output = "[Passenger:%s]" % self.id

        # check if dictionary is empty
        if not self.journey_history:
            return output + "\n\n"

        for key, value in self.journey_history.items():
            if value == "Detrain":
                output += "\n%s Detrain" % key
            else:
                output += "\n%s Board %s" % (str(key), value)

        return output + "\n\n"
