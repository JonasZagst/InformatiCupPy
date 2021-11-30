class Passenger:

    def __init__(self, id, initial_station, target_station, group_size, target_time):
        # id of the passanger
        self.id = id
        # start station of this passanger
        self.initialStation = initial_station
        # target station of this passanger
        self.targetStation = target_station
        # this is the number of persons eventually traveling with this passanger
        self.groupSize= group_size
        # the target time of arrival
        self.targetTime = target_time

    def to_string(self):
        return "%s %s %s %s %s" % (self.id, self.initialStation, self.targetStation, self.groupSize, self.targetTime)
