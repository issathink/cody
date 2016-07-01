class Timelink(object):
    node_a = -1;
    node_b = -1;
    time = -1;

    def __init__(self, node_a, node_b, time):
        self.node_a = node_a
        self.node_b = node_b
        self.time = time

    def __str__(self):
        return "[" + str(self.node_a) + " " + str(self.node_b) + " " + str(self.time) + "]"

    @classmethod
    def create(cls, node_a, node_b, time):
        return Timelink(node_a, node_b, time)
