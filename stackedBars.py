import matplotlib.pyplot as plt
import numpy as np
import statistics as st

dataSets = 4

file = open("../timeDistribution.txt", "r")

width = 0.4
#colors = [(1,0,0), (0,1,0), (0,0,1), (0,1,1), (1,0,1), (1,1,0)]
colors = ['r', 'g', 'b', 'c', 'm', 'y']
phases = ["read data", "insert into tree", "dbscan", "print data"]
colors = colors[0:len(phase)]

names = []
columns = []
columnsAggr = []
columnsError = []
columnsPercent = []
columnsPercentAggr = []
plt.figure(dpi=300)
for line in file:
    line = line.strip("\n ")
    lineSplit = line.split(";")

    data = np.reshape(list(map(lambda x:float(x), lineSplit[1::])), (4,-1), order='F')

    column = list(map(lambda x:st.mean(x), data))
    columnAggr = list(sum(column[0:x:]) for x in range(len(column)))
    errorbar = list(map(lambda x:st.stdev(x), data))

    total = sum(column)
    columnPercent = list((x/total) for x in column)
    columnPercentAggr = list(sum(columnPercent[0:x:]) for x in range(len(columnPercent)))

    columns.append(column)
    columnsAggr.append(columnAggr)
    columnsError.append(errorbar)
    columnsPercent.append(columnPercent)
    columnsPercentAggr.append(columnPercentAggr)
    names.append(lineSplit[0].split("$")[1])
#plt.show()
#print(str(columns))
rows = np.swapaxes(columns, 0, 1)
rowsAggr = np.swapaxes(columnsAggr, 0, 1)
rowsErr = np.swapaxes(columnsError, 0, 1)
rowsPercent = np.swapaxes(columnsPercent, 0, 1)
rowsPercentAggr = np.swapaxes(columnsPercentAggr, 0, 1)

bars = []
indexes = np.arange(len(names))
for i in range(len(rows)):
    bars.append(plt.bar(indexes, rows[i], width, bottom=rowsAggr[i], yerr=rowsErr[i], color=colors[i]))
plt.ylabel('Execution Time in μs')
plt.xticks(indexes, names)
plt.legend(bars[::-1], phases[::-1])
plt.savefig("test.png", dpi=600)
plt.show()

bars = []
indexes = np.arange(len(names))
for i in range(len(rowsPercent)):
    bars.append(plt.bar(indexes, rowsPercent[i], width, bottom=rowsPercentAggr[i], color=colors[i]))
plt.xticks(indexes, names)
plt.legend(bars[::-1], phases[::-1])
plt.show()
