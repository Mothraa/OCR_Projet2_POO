from datetime import datetime
import csv

def create_directory(directory_path):
    """from a path name, create a directory
    Args:
     directory_path: path name
    Returns:
     None
    """
    directory_path.mkdir(parents=True, exist_ok=True)


def save_file(file_path, data):

    file_path.touch(exist_ok=True)
    file_path.write_bytes(data)

#    del page1.image_data