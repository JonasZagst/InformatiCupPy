class Train:

    def __init__(self, id, position, speed, capacity):
        # every train has a train ID
        self.id = id
        # number of passanger, which can travel with this train
        self.capacity = capacity
        # passangers of this train
       # self.passengers
        # speed of this train
        self.speed = speed
        # current position of this train
        self.position = position
        #self.position_since
        #self.position_type
       # self.plan
        #self.boarding_possible

    def to_string(self):
        return "%s %s %s %s" % (self.id, self.position, self.speed, self.capacity)

