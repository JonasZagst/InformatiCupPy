class Station:

    def __init__(self, id, capacity):
        #station id
        self.id = id
        # Capacity in trains at the same time
        self.capacity = capacity

    def to_string(self) -> str:
        return "%s %s" % (self.id, self.capacity)
