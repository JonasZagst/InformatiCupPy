class Lane:

    def __init__(self, id, connected_stations, length, capacity):
        self.id = id
        # Array of fixed length 2 of both end stations.
        self.connected_stations = connected_stations
        # Decimal length of the lane
        self.length = length
        # Capacity in trains at the same time
        self.capacity = capacity

    def to_string(self):
        return "%s %s %s %s %s" % (self.id,
                                   self.connected_stations[0],
                                   self.connected_stations[1],
                                   self.length,
                                   self.capacity)