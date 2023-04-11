import sys
import os
import shutil
import zipfile


def normalize(name):
    """Normalize file/folder names"""
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
    result = ''
    for char in name:
        if char.isalpha() and (char.lower() in translit_dict):
            # Transliterate characters
            char = translit_dict[char.lower()]
            if name.isupper():
                char = char.upper()
            elif name.istitle():
                char = char.title()
        elif char not in allowed_chars:
            # Replace non-alphanumeric characters
            char = '_'
        result += char
    return result



def sort_folder(folder_path):
    """Sort files in the folder based on their extensions"""
    images = ['JPEG', 'PNG', 'JPG', 'SVG']
    videos = ['AVI', 'MP4', 'MOV', 'MKV']
    docs = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    music = ['MP3', 'OGG', 'WAV', 'AMR']
    archives = ['ZIP', 'GZ', 'TAR']

    known_extensions = set()  # Set of known extensions
    unknown_extensions = set()  # Set of unknown extensions

    # Iterate through all files and folders in the directory
    for item in os.scandir(folder_path):
        # Ignore directories starting with '.'
        if item.name.startswith('.'):
            continue

        # Normalize file/folder name
        new_name = normalize(item.name)

        if item.is_file():
            # Get file extension
            file_extension = os.path.splitext(item.name)[1][1:].upper()
            # Add extension to the corresponding set
            if file_extension in images:
                folder_name = 'images'
            elif file_extension in videos:
                folder_name = 'videos'
            elif file_extension in docs:
                folder_name = 'documents'
            elif file_extension in music:
                folder_name = 'audio'
            elif file_extension in archives:
                folder_name = 'archives'
            else:
                folder_name = None
                unknown_extensions.add(file_extension)

            # Move file to the corresponding folder
            if folder_name:
                known_extensions.add(file_extension)
                folder_path = os.path.join(os.path.dirname(item.path), folder_name)
                os.makedirs(folder_path, exist_ok=True)
                new_path = os.path.join(folder_path, new_name)
                shutil.move(item.path, new_path)
        elif item.is_dir():
            # Recursively process subfolders
            subfolder_path = os.path.join(os.path.dirname(item.path), new_name)
            sort_folder(subfolder_path)

    # Unpack archives and move files to the corresponding folder
    for item in os.scandir(os.path.join(folder_path, 'archives')):
        if item.is_file():
            file_extension = os.path.splitext(item.name)[1][1:].upper()
            if file_extension in archives:
                folder_name = os.path.splitext(new_name)[0]
                folder_path = os.path.join(os.path.dirname(item.path), folder_name)
                os.makedirs(folder_path, exist_ok=True)
                shutil.unpack_archive(item.path, folder_path)
                os.remove(item.path)

    # Delete empty folders
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Print results
    print(f"List of files in images: {os.listdir(os.path.join(folder_path, 'images'))}")
    print(f"List of files in videos: {os.listdir(os.path.join(folder_path, 'videos'))}")
    print(f"List of files in documents: {os.listdir(os.path.join(folder_path, 'documents'))}")
    print(f"List of files in archives: {os.listdir(os.path.join(folder_path, 'archives'))}")
    print(f"List of files in audio: {os.listdir(os.path.join(folder_path, 'audio'))}")
