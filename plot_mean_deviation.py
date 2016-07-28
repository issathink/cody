import time
from src.tool import plot_mean_and_deviation


filename = "enron.dyn"  # "enron"
each = 1209600  # 240
delta = 3628800  # 3628800  # 604800
start = time.time()
directory = "./data/deviation/"

plot_mean_and_deviation(directory, filename, each, None)

print "Time elapsed: " + str(time.time() - start)
