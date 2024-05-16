def append_to_file(filename, data):
    # Replace potential ':' characters with '_'
    filename = filename.replace(':', '_')

    try:
        # Open the file in append mode, creating it if it doesn't exist
        with open(f'data/{filename}', 'a') as file:
            # Convert data to float and then write it to the file
            file.write(str(float(data)) + '\n')  # Assuming each data entry is written on a new line
        print("Data appended to", filename)
    except FileNotFoundError:
        print("File not found. Creating a new file...")
        # Create a new file and write the data
        with open(filename, 'w') as file:
            file.write(str(float(data)) + '\n')
        print("Data written to new file:", filename)
