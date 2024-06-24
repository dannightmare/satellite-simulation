import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("historyNS.txt", delimiter=",")

print(np.unique(data[:, 1]))

plt.hist(data[:, 1], bins=[8, 9, 10, 11])
plt.xticks([8, 9, 10], horizontalalignment='left')
plt.title('Number of satellite hops (North - South poles)')
plt.ylabel('number of simulations')
plt.show()

plt.hist(data[:, 0] / 3)
plt.title('latency (North - South poles)')
plt.ylabel('number of simulations')
plt.xlabel('miliseconds (ms)')
plt.show()
