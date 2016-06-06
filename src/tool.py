from src.timelink import Timelink

"""
    Check if 's' is a string of digit.
    @:param s - the string to verify
    @:return true or false
"""
def check_int(s):
    if s[0] in ('+'):
    	return s[1:].isdigit()
    return s.isdigit()

"""
    Given a file, return list of time links
"""
def get_time_links(filename):
    l = []
    v = set()

    with open(filename, "r") as elems:
        for elem in elems:
            tmp = elem.split(" ")
            time = int(tmp[2])
            nodeA = int(tmp[0])
            nodeB = int(tmp[1])
            timelink = Timelink.create(nodeA, nodeB, time)  # make_timelink(nodeA, nodeB, time)
            l.append(timelink)
            v.add(nodeA)
            v.add(nodeB)

    return (l,v)


def get_time_low(l, time):
    return filter(lambda e: e.time < time, l)


def get_time_up(l, time):
    return filter(lambda e: e.time > time, l)