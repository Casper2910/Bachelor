import importlib.util


def insert_entry(identifier, name):
    try:
        spec = importlib.util.spec_from_file_location("id_dict", "id_dict.py")
        id_dict_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(id_dict_module)

        id_dict_module.id_dict[identifier] = name

        with open("id_dict.py", "w") as f:
            f.write("id_dict = " + repr(id_dict_module.id_dict))
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


if __name__ == "__main__":
    insert_entry(2, 'did:test:test12345')

    id1 = find_id('did:test:test123')
    id2 = find_id('did:test:test12345')
    id3 = find_id('did:test:test1222345')

    print(id1)
    print(id2) 
    print(id3)
