from InformatiCupPy.com.informaticup.python.algorithms.Helper import Helper


class Train:
    """Class representation for trains"""

    def __init__(self, original_id, original_position, speed, capacity):
        self.id = ""
        self.original_id = original_id
        self.capacity = int(capacity)
        self.passengers = None
        self.speed = float(speed)
        self.position = ""
        self.original_position = original_position
        self.initial_position = self.position
        self.fixed_start = True
        self.journey_history = {}

    def to_string(self):
        """Returns objects properties as String fitting the input format."""

        return "%s %s %s %s" % (self.id, self.position, self.speed, self.capacity)

    def to_output(self, input):
        """Returns objects properties as String fitting the output format."""

        output = "[Train:%s]" % self.original_id

        # check if dictionary is empty
        if not self.journey_history:
            return output + "\n\n"

        if self.initial_position != "":
            initial = Helper.get_element_from_list_by_id(self.initial_position, input[0])

        for key, value in self.journey_history.items():
            if value.startswith("L"):
                self.journey_history[key] = Helper.get_element_from_list_by_id(value, input[1]).original_id

        # check if start was fixed
        # if start was fixed it hast to be in the output file
        # if not it isn´t allowed to be in the output file
        if not self.fixed_start:
            output += "\n0 Start %s" % initial.original_id

        for key, value in self.journey_history.items():
            output += "\n%s Depart %s" % (str(key), value)

        return output + "\n\n"

    def set_internal_id(self, id):
        self.id = id

    def set_internal_position(self, internal_position):
        if internal_position == "*":
            self.fixed_start = False
        self.position = internal_position

    def get_original_position(self):
        return self.original_position
