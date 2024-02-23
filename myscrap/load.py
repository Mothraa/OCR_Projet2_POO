import shutil

def save_image_file(file_path, data):

    with open(file_path, 'wb') as file: #directory + file_name
        shutil.copyfileobj(data, file)
#    del page1.image_data