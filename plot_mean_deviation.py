import time
from src.tool import plot_mean_and_deviation


filename = "rollernet.dyn"  # "enron.dyn"
each = 240
delta = 240  # 3628800  # 604800
start = time.time()
directory = "./data/deviation/"

plot_mean_and_deviation(directory, filename, each, None)
