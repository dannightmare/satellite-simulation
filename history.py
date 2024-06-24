import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("history.txt", delimiter=",")


print(np.unique(data[:, 1]))

plt.hist(data[data[:, 1] == 5, 1], bins=[5, 6, 7], color='orange')
plt.hist(data[data[:, 1] == 6, 1], bins=[5, 6, 7], color='cyan')
plt.xticks([5, 6], horizontalalignment='left')
plt.title('Number of satellite hops (TelHai - NY)')
plt.ylabel('number of simulations')
plt.show()

plt.hist(data[:, 0] / 3, color='turquoise')
plt.title('latency (TelHai - NY)')
plt.ylabel('number of simulations')
plt.xlabel('miliseconds (ms)')
plt.show()
