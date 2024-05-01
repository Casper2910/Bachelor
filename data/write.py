def append_to_file(filename, data):
    try:
        # Open the file in append mode, creating it if it doesn't exist
        with open(filename, 'a') as file:
            # Write the data to the file
            file.write(data + '\n')  # Assuming each data entry is written on a new line
        print("Data appended to", filename)
    except FileNotFoundError:
        print("File not found. Creating a new file...")
        # Create a new file and write the data
        with open(filename, 'w') as file:
            file.write(data + '\n')
        print("Data written to new file:", filename)

