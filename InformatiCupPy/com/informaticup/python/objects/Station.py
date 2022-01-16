class Station:
    """Class representation for stations"""

    def __init__(self, original_id, capacity):
        self.id = ""
        self.original_id = original_id
        self.capacity = int(capacity)

    def to_string(self) -> str:
        """Returns objects properties as String fitting the input format."""

        return "%s %s" % (self.id, self.capacity)

    def set_internal_id(self, id):
        self.id = id

    def get_internal_id(self):
        return self.id

    def get_original_id(self):
        return self.original_id
