import csv
import matplotlib.pyplot as plt
import numpy as np

def calculate_average_csv(file_path):
    total = 0
    count = 0

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for value in row:
                try:
                    total += float(value)
                    count += 1
                except ValueError:
                    # Ignore rows where the value cannot be converted to float
                    pass

    if count == 0:
        return None
    return total / count


# DID generation
did1 = calculate_average_csv("test/did_1.csv")
did10 = calculate_average_csv("test/did_10.csv")
did20 = calculate_average_csv("test/did_20.csv")
did40 = calculate_average_csv("test/did_40.csv")
did60 = calculate_average_csv("test/did_60.csv")
did80 = calculate_average_csv("test/did_80.csv")
did100 = calculate_average_csv("test/did_100.csv")

# DID document generation
did_doc1 = calculate_average_csv("test/did_doc_1.csv")
did_doc10 = calculate_average_csv("test/did_doc_10.csv")
did_doc20 = calculate_average_csv("test/did_doc_20.csv")
did_doc40 = calculate_average_csv("test/did_doc_40.csv")
did_doc60 = calculate_average_csv("test/did_doc_60.csv")
did_doc80 = calculate_average_csv("test/did_doc_80.csv")
did_doc100 = calculate_average_csv("test/did_doc_100.csv")

# DID serialization
did_ser1 = calculate_average_csv("test/serializeDID_1.csv")
did_ser10 = calculate_average_csv("test/serializeDID_10.csv")
did_ser20 = calculate_average_csv("test/serializeDID_20.csv")
did_ser40 = calculate_average_csv("test/serializeDID_40.csv")
did_ser60 = calculate_average_csv("test/serializeDID_60.csv")
did_ser80 = calculate_average_csv("test/serializeDID_80.csv")
did_ser100 = calculate_average_csv("test/serializeDID_100.csv")

# DID document serialization
did_doc_ser1 = calculate_average_csv("test/serializeDID_doc_1.csv")
did_doc_ser10 = calculate_average_csv("test/serializeDID_doc_10.csv")
did_doc_ser20 = calculate_average_csv("test/serializeDID_doc_20.csv")
did_doc_ser40 = calculate_average_csv("test/serializeDID_doc_40.csv")
did_doc_ser60 = calculate_average_csv("test/serializeDID_doc_60.csv")
did_doc_ser80 = calculate_average_csv("test/serializeDID_doc_80.csv")
did_doc_ser100 = calculate_average_csv("test/serializeDID_doc_100.csv")

categories = [1, 10, 20, 40, 60, 80, 100]
did_values = [did1 / 1000, did10 / 1000, did20 / 1000, did40 / 1000, did60 / 1000, did80 / 1000, did100 / 1000]
did_doc_values = [did_doc1 / 1000, did_doc10 / 1000, did_doc20 / 1000, did_doc40 / 1000, did_doc60 / 1000, did_doc80 / 1000, did_doc100 / 1000]
did_ser_values = [did_ser1 / 1000, did_ser10 / 1000, did_ser20 / 1000, did_ser40 / 1000, did_ser60 / 1000, did_ser80 / 1000, did_ser100 / 1000]
did_doc_ser_values = [did_doc_ser1 / 1000, did_doc_ser10 / 1000, did_doc_ser20 / 1000, did_doc_ser40 / 1000, did_doc_ser60 / 1000, did_doc_ser80 / 1000, did_doc_ser100 / 1000]

print("did_values")
for did in did_values:
    print(did)

print("did_doc_values")
for did in did_doc_values:
    print(did)

print("did_ser_values")
for did in did_ser_values:
    print(did)

print("did_doc_ser_values")
for did in did_doc_ser_values:
    print(did)

# Sample data for boxplot
vc_data = []
with open('test/vc.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        vc_data.append([float(value) for value in row])

# Number of categories
n = len(categories)

# Create an array with the positions of each group
ind = np.arange(n)

# Width of a single bar
width = 0.2

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each set of bars
rects1 = ax.bar(ind - width*1.5, did_values, width, label='DID generation', color='blue')
rects2 = ax.bar(ind - width*0.5, did_doc_values, width, label='DID document generation', color='green')
rects3 = ax.bar(ind + width*0.5, did_ser_values, width, label='DID serialization', color='red')
rects4 = ax.bar(ind + width*1.5, did_doc_ser_values, width, label='DID doc serialization', color='purple')

# Add labels, title, and custom x-axis tick labels
ax.set_xlabel('Amount of DID and DID documents per Arduino')
ax.set_ylabel('Time in milliseconds')
ax.set_title('DID and DID doc generation performance')
ax.set_xticks(ind)
ax.set_xticklabels(categories)
ax.legend()

# Adjust layout
plt.tight_layout()
plt.show()