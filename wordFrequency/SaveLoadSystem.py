import pickle
from scrollableTable import TextPath



def save_objects_to_dict(object_list, filename):
    objects_dict = {}

    # Storing objects in the dictionary
    for i, obj in enumerate(object_list, start=1):
        objects_dict[f"Object{i}"] = obj

    # Save the dictionary to a file using pickle
    with open(filename, 'wb') as file:
        pickle.dump(objects_dict, file)

    return objects_dict


def load_objects_from_file(filename):
    # Load the dictionary from the file using pickle
    with open(filename, 'rb') as file:
        objects_dict = pickle.load(file)

    return objects_dict


if __name__ == "__main__":
    save_objects_to_dict([],'Data.pkl')

    # Create a list of 10 objects using a loop
    object_list = []
    for i in range(1, 11):
        instance = TextPath(f"Path{i}", f"Title{i}", f"About{i}")
        object_list.append(instance)

    # Save objects to a dictionary and a file
    save_filename = "objects_dict.pkl"
    objects_dict = save_objects_to_dict(object_list, save_filename)

    # Displaying the saved objects
    for key, value in objects_dict.items():
        print(f"{key}: {value.path}, {value.title}, {value.about}")

    # Load objects from the file
    loaded_objects_dict = load_objects_from_file(save_filename)

    # Displaying the loaded objects
    print("\nLoaded Objects:")
    for key, value in loaded_objects_dict.items():
        print(f"{key}: {value.path}, {value.title}, {value.about}")