"""A helper module containing methods for exporting data.

Provides the necessary tools to export an object to either a csv or json file.

"""


import csv
import json


def export_to_csv(obj, file_name):
    """Export a list of dictionaries to a csv file.

    Args:
    =====
    obj (list): A list of dictionaries representing the object to be exported
    file_name (str): The destination file name

    """
    keys = obj[0].keys()
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(obj)


def export_to_json(obj, file_name):
    """Export a list of dictionaries to a json file.

    Args:
    =====
    obj (list): A list of dictionaries representing the object to be exported
    file_name (str): The destination file name

    """
    with open(file_name, 'w') as output_file:
        json.dump(obj, output_file)
