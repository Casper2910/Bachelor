import importlib.util


def insert_entry(identifier, name):
    try:
        # Create a spec from the file location
        spec = importlib.util.spec_from_file_location("id_dict", "id_dict.py")

        # Import the module
        id_dict_module = importlib.util.module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(id_dict_module)

        # Modify the dictionary
        id_dict_module.id_dict[identifier] = name

        # Convert the dictionary to a formatted string
        id_dict_str = "id_dict = {\n"
        for key, value in id_dict_module.id_dict.items():
            id_dict_str += f"    {repr(key)}: {repr(value)},\n"
        id_dict_str += "}"

        # Write the modified dictionary back to the file
        with open("id_dict.py", "w") as f:
            f.write(id_dict_str)
    except FileNotFoundError:
        print("ID dictionary file not found.")


def find_id(name):
    try:
        spec = importlib.util.spec_from_file_location("id_dict", "id_dict.py")
        id_dict_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(id_dict_module)

        for identifier, stored_name in id_dict_module.id_dict.items():
            if stored_name == name:
                return identifier
        return None
    except FileNotFoundError:
        print("ID dictionary file not found.")


def add_to_blacklist(name):
    try:
        # Create a spec from the file location
        spec = importlib.util.spec_from_file_location("blacklist", "blacklist.py")

        # Import the module
        blacklist_module = importlib.util.module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(blacklist_module)

        # Modify the list
        blacklist_module.blacklist.append(name)

        # Convert the list to a formatted string
        blacklist_str = "blacklist = [\n"
        for item in blacklist_module.blacklist:
            blacklist_str += f"    '{item}',\n"
        blacklist_str += "]"

        # Write the formatted string back to the file
        with open("blacklist.py", "w") as file:
            file.write(blacklist_str)
    except Exception as e:
        print(f"An error occurred: {e}")


def is_blacklisted(name):
    from blacklist import blacklist
    for did in blacklist:
        if did == name:
            return True

    return False


def add_to_queue_list(name):
    try:
        # Create a spec from the file location
        spec = importlib.util.spec_from_file_location("queue_list", "queue_list.py")

        # Import the module
        queue_list_module = importlib.util.module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(queue_list_module)

        # Modify the list
        queue_list_module.queue_list.append(name)

        # Convert the list to a formatted string
        queue_list_str = "queue_list = [\n"
        for item in queue_list_module.queue_list:
            queue_list_str += f"    '{item}',\n"
        queue_list_str += "]"

        # Write the formatted string back to the file
        with open("queue_list.py", "w") as file:
            file.write(queue_list_str)
    except Exception as e:
        print(f"An error occurred: {e}")

def pop_queue_list():
    try:
        # Create a spec from the file location
        spec = importlib.util.spec_from_file_location("queue_list", "queue_list.py")

        # Import the module
        queue_module = importlib.util.module_from_spec(spec)

        # Load the module
        spec.loader.exec_module(queue_module)

        # Pop the first element from the list if it's not empty
        if queue_module.queue_list:
            queue_module.queue_list.pop(0)

            # Convert the list to a formatted string
            queue_list_str = "queue_list = [\n"
            for item in queue_module.queue_list:
                queue_list_str += f"    '{item}',\n"
            queue_list_str += "]"

            # Write the formatted string back to the file
            with open("queue_list.py", "w") as file:
                file.write(queue_list_str)
        else:
            print("The queue list is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

