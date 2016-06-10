import sys
import os
import time
from os.path import isfile
from src.tool import check_int
from src.tool import get_time_links
from src.tool import generate_plot_file
from src.method_one import compute_nb_in_out
from src.method_one import compute_nb_in_out_array
from src.method_one import compute_vertex_nb_in
from src.method_one import compute_vertex_nb_out


"""
    Entry point
"""

# args = sys.stdin.readline().split(" ")
args = "../data/enron.dyn 0 98277035".split(" ")

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

(links, vertexes) = get_time_links(filename, instant)
nb_vertexes = len(vertexes)

start = time.time()


print "\n####### nb_in/out matrix: #########"
result = compute_nb_in_out(links, nb_vertexes)
generate_plot_file("rollernet", result)
for i in range(len(result)):
    print "(nb_in, nb_out)[" + str(i) + "][" + str(instant) + "] = " + str(result[i])
print "\n$$$ nb_in/out matrix: " + str(time.time() - start) + " sec"


# This is version is slightly slower than the previous one
# but resolves the memory limitation
print "\n####### nb_in/out array: #########"
st1 = time.time()
result = compute_nb_in_out_array(links, nb_vertexes)
for i in range(len(result)):
    print "(nb_in, nb_out)[" + str(i) + "][" + str(instant) + "] = " + str(result[i])
print "\n$$$ nb_in/out array: " + str(time.time() - st1) + " sec"


st1 = time.time()
print "\n########## nb_in: ###########"
for i in range(nb_vertexes):
    res = compute_vertex_nb_in(links, nb_vertexes, i)
    if len(res[1]) < 10:
        print "nb_in[" + str(i) + "] = " + str(res)
    else:
        print "nb_in[" + str(i) + "] = " + str(res[0])
print "\n$$$ nb_in: " + str(time.time() - st1) + " sec"


"""
st1 = time.time()
print "\n######### nb_out: ###########"
for i in range(nb_vertexes):
    res = compute_vertex_nb_out(links, nb_vertexes, i)
    if len(res[1]) < 10:
        print "nb_out[" + str(i) + "] = " + str(res)
    else:
        print "nb_out[" + str(i) + "] = " + str(res[0])
print "\n$$$ nb_out: " + str(time.time() - st1) + " sec"
"""

end = time.time()
print "\nTime elapsed: " + str(end-start) + " sec(s)"

