from src.tool import plot_in_out_for_each_instant

# Generate plot files at each instant of time links.

each = 240
filename = "rollernet.dyn"
directory = "./data/each_instant/"

plot_in_out_for_each_instant(directory, filename, each)
plot_in_out_for_each_instant(directory, filename, each=360)

filename = "enron.dyn"
each = 3628800

plot_in_out_for_each_instant(directory, filename, each)
