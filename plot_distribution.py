import time

from src.tool import get_time_links
from src.tool import plot_in_out_distribution
from src.method_one import compute_nb_in_out
from src.method_one import nb_in_out_delta

filename = "rollernet.dyn"
each = 1000
delta = 3628800  # 604800
with_delta = False
start = time.time()

instants = set()
(links, nb_vertexes) = get_time_links("./data/" + filename)

for elem in links:
    instants.add(elem.time)

print "Length of instants: " + str(len(instants))
instants = list(instants)
instants.sort()

print instants[0]
print instants[len(instants)-1]

if with_delta:
    for i in range(len(instants)):
        if instants[i] > delta:
            break
    for j in reversed(xrange(len(instants)-1)):
        if instants[j]+delta < instants[len(instants)-1]:
            break

    print str(i) + ": " + str(instants[i]) + " " + str(j) + ": " + str(instants[j])
    for k in range(i, j, each):
        result = nb_in_out_delta("./data/" + filename, instants[k], delta)
        plot_in_out_distribution(filename + str(k) + "_nb_in", result, True)
        plot_in_out_distribution(filename + str(k) + "_nb_out", result, None)
        print "> " + str(k)
else:
    for i in range(1, len(instants), each):
        result = nb_in_out_delta("./data/" + filename, instants[i], delta)
        plot_in_out_distribution(filename + str(i) + "_nb_in", result, True)
        plot_in_out_distribution(filename + str(i) + "_nb_out", result, None)
        print "> " + str(i)

print "\nTime elapsed: " + str(time.time()-start) + " sec(s)"
