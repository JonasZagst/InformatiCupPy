class Train:

    def __init__(self, id, position, speed, capacity):
        # every train has a train ID
        self.id = id
        # number of passenger, which can travel with this train
        self.capacity = capacity
        # passengers of this train
        self.passengers = None
        # speed of this train
        self.speed = speed
        # current position of this train
        self.position = position
        # self.position_since
        # self.position_type
        # self.plan
        # self.boarding_possible
        self.initial_position = position
        self.fixed_start = True
        self.journey_history = {}
        if position == "*":
            self.fixed_start = False

    """Returns objects properties as String fitting the input format."""

    def to_string(self):
        return "%s %s %s %s" % (self.id, self.position, self.speed, self.capacity)

    """Returns objects properties as String fitting the output format."""

    def to_output(self):
        output = "[Train:%s]" % self.id

        # check if dictionary is empty
        if not self.journey_history:
            return output + "\n\n"

        # check if start was fixed
        # if start was fixed it hast to be in the output file
        # if not it isn´t allowed to be in the output file
        if not self.fixed_start:
            output += "\n0 Start %s" % self.initial_position

        for key, value in self.journey_history.items():
            output += "\n%s Depart %s" % (str(key), value)

        return output + "\n\n"
