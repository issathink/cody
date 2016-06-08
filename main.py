import sys
import os
import time
from os.path import isfile
from src.tool import check_int
from src.method_one import compute_nb_in_out
from src.method_one import compute_vertex_nb_in
from src.method_one import compute_vertex_nb_out

"""
    Entry point
"""

# args = sys.stdin.readline().split(" ")
args = "../data/test2.dyn 0 99999999".split(" ")

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

start = time.time()

print "\n####### nb_in/out: #########"
result = compute_nb_in_out(filename, instant)
for i in range(len(result)):
    print "(nb_in, nb_out)[" + str(i) + "][" + str(instant) + "] = " + str(result[i])

print "\n########## nb_in: ###########"
for i in range(4):
    print "nb_in[" + str(i) + "] = " + str(compute_vertex_nb_in(filename, instant, i))

print "\n######### nb_out: ###########"
for i in range(4):
    print "nb_out[" + str(i) + "] = " + str(compute_vertex_nb_out(filename, instant, i))

end = time.time()
print "\nTime elapsed: " + str(end-start) + " sec(s)"
