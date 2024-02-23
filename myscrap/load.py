from datetime import datetime
import csv

def create_directory(directory_path):
    """from a path name, create a directory
    Args:
     directory_path: path name
    Returns:
     None
    """
    
#    os.makedirs(directory_path, exist_ok=True)

    directory_path.mkdir(parents=True, exist_ok=True)
    return None


def save_file(file_path, data):

    # with open(file_path, 'wb') as file: #directory + file_name
    #     shutil.copyfileobj(data, file)

    file_path.touch(exist_ok=True)
    file_path.write_bytes(data)

#    del page1.image_data