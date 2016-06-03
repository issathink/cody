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
    with open(filename, "r") as elems:
        for elem in elems:
            tmp      = elem.split(" ")
            nodeA    = int(tmp[0])
            nodeB    = int(tmp[1])
            time     = int(tmp[2])
            timelink = Timelink.create(nodeA, nodeB, time) # make_timelink(nodeA, nodeB, time)

            l.append(timelink)

    return l

def get_time_limited(l, time):
    return filter(lambda e: e.time < time, l)