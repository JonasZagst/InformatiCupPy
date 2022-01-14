class Line:
    """Class representation for lines"""

    def __init__(self, original_id, original_connected_stations, length, capacity):
        self.id = ""
        self.original_id = original_id
        self.original_connected_stations = original_connected_stations
        # Array of fixed length 2 of both end stations.
        self.connected_stations = []
        # Decimal length of the lane
        self.length = float(length)
        # Capacity in trains at the same time
        self.capacity = int(capacity)
        # Current capacity (capacity - trains on line)
        self.current_capacity = int(capacity)

    def to_string(self):
        """Returns objects properties as String fitting the input format."""
        return "%s %s %s %s %s" % (self.id,
                                   self.connected_stations[0],
                                   self.connected_stations[1],
                                   self.length,
                                   self.capacity)

    def set_internal_id(self, id):
        self.id = id

    def set_internal_connected_stations(self, connected_stations):
        self.connected_stations = connected_stations

    def get_original_connected_stations(self):
        return self.original_connected_stations
