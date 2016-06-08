class Timelink(object):
    nodeA = -1;
    nodeB = -1;
    time = -1;

    def __init__(self, nodeA, nodeB, time):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.time  = time

    def __str__(self):
        return "[" + str(self.nodeA) + " " + str(self.nodeB) + " " + str(self.time) + "]"

    @classmethod
    def create(self, nodeA, nodeB, time):
        return Timelink(nodeA, nodeB, time)
