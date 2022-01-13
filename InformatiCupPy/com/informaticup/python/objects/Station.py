class Station:

    def __init__(self, original_id, capacity):
        # station id
        self.id = ""
        self.original_id = original_id
        # Capacity in trains at the same time
        self.capacity = int(capacity)

    def to_string(self) -> str:
        return "%s %s" % (self.id, self.capacity)

    def set_internal_id(self, id):
        self.id = id

    def get_internal_id(self):
        return self.id

    def get_original_id(self):
        return self.original_id