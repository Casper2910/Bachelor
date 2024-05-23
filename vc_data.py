import csv
import matplotlib.pyplot as plt
import numpy as np

vc_data = []
with open('test/vc.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # Convert the single value in the row to float
        float_value = float(row[0])
        vc_data.append(float_value)

print("average: ", np.average(vc_data))
print("mean: ", np.mean(vc_data))

fig = plt.figure(figsize =(12, 6))

plt.boxplot(vc_data, vert=False)
# Set x-axis ticks to be more granular
plt.xticks(np.arange(0, max(vc_data) + 1, step=1))
# Adjust the padding between ticks and boxplot
plt.tick_params(axis='x', pad=5)  # Change the value of pad as needed

plt.show()