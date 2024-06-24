import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("historyNS.txt", delimiter=",")

print(np.unique(data[:, 1]))

plt.hist(data[data[:, 1] == 8, 1], bins=[8, 9, 10, 11], color='orange')
plt.hist(data[data[:, 1] == 9, 1], bins=[8, 9, 10, 11], color='magenta')
plt.hist(data[data[:, 1] == 10, 1], bins=[8, 9, 10, 11], color='blue')
plt.xticks([8, 9, 10], horizontalalignment='left')
plt.title('Number of satellite hops (North - South poles)')
plt.ylabel('number of simulations')
plt.show()

plt.hist(data[:, 0] / 3)
plt.title('latency (North - South poles)')
plt.ylabel('number of simulations')
plt.xlabel('miliseconds (ms)')
plt.show()
