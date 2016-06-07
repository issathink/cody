import sys, os, time
from os.path import isfile
from src.tool import check_int
from src.method_one import algo

"""
    Entry point.
"""

# args = sys.stdin.readline().split(" ")
args = "../data/test2.dyn 0 9999999999".split(" ")

if len(args) <= 2:
    print "Usage:  filename  vertex_id (>0)  time (>0)"
    sys.exit(-1)

if (not isfile(args[0])) or (not os.access(args[0], os.R_OK)):
    print "File '" + args[0] + "' doesn't exist or locked."
    sys.exit(-1)

if (not check_int(args[1])) or (not check_int(args[2].strip())):
    print "Positive int are expected for vertex_id and time."
    sys.exit(-1)

filename = args[0]
vertex_id = int(args[1])
instant = int(args[2].strip())

# test(filename) #, vertex_id, time)
# test_time(filename, 98277034)

start = time.time()
result = algo(filename, instant)

#for i in range(len(result)):
#    print "(nb_in, nb_out)[" + str(i) + "][" + str(instant) + "] = " + str(result[i])

end = time.time()
print "\nTime elappsed: " + str(end-start) + " sec(s)"

# print "(nb_out, nb_in)[1][" + str(time) + "] = " + str(algo(filename, 1, time))
# print "(nb_out, nb_in)[2][" + str(time) + "] = " + str(algo(filename, 2, time))
# print "(nb_out, nb_in)[3][" + str(time) + "] = " + str(algo(filename, 3, time))
