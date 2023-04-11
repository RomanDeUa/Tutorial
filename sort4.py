import os
import shutil
import zipfile

IMAGE_EXTENSIONS = ['JPEG', 'JPG', 'PNG', 'SVG']
VIDEO_EXTENSIONS = ['AVI', 'MP4', 'MOV', 'MKV']
DOCUMENT_EXTENSIONS = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
MUSIC_EXTENSIONS = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVE_EXTENSIONS = ['ZIP', 'GZ', 'TAR']

def normalize(text):
    translation_table = str.maketrans(
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        'abvgdeejzijklmnoprstufhzcss_y_eua')
    normalized = text.translate(translation_table)
    normalized = ''.join(c if c.isalnum() else '_' for c in normalized)
    return normalized

def handle_file(filepath):
    extension = os.path.splitext(filepath)[1][1:].upper()
    if extension in IMAGE_EXTENSIONS:
        target_folder = 'images'
    elif extension in VIDEO_EXTENSIONS:
        target_folder = 'videos'
    elif extension in DOCUMENT_EXTENSIONS:
        target_folder = 'documents'
    elif extension in MUSIC_EXTENSIONS:
        target_folder = 'audio'
    elif extension in ARCHIVE_EXTENSIONS:
        target_folder = 'archives'
        foldername = os.path.splitext(os.path.basename(filepath))[0]
        target_folder = os.path.join(target_folder, foldername)
        os.makedirs(target_folder, exist_ok=True)
        with zipfile.ZipFile(filepath, 'r') as ziphandle:
            ziphandle.extractall(target_folder)
        return
    else:
        print(f'Unknown extension: {extension}')
        return
    filename = os.path.basename(filepath)
    newname = normalize(os.path.splitext(filename)[0]) + '.' + extension
    newpath = os.path.join(target_folder, newname)
    shutil.move(filepath, newpath)

def handle_folder(folderpath):
    for entry in os.listdir(folderpath):
        fullpath = os.path.join(folderpath, entry)
        if os.path.isfile(fullpath):
            handle_file(fullpath)
        elif os.path.isdir(fullpath) and entry not in ['archives', 'videos', 'audio', 'documents', 'images']:
            handle_folder(fullpath)

if __name__ == '__main__':
    folder = input('Enter the folder path to analyze: ')
    image_files = []
    video_files = []
    document_files = []
    music_files = []
    archive_files = []
    unknown_files = []
    handle_folder(folder)
    for entry in os.listdir(folder):
        fullpath = os.path.join(folder, entry)
        if os.path.isfile(fullpath):
            extension = os.path.splitext(entry)[1][1:].upper()
            if extension in IMAGE_EXTENSIONS:
                image_files.append(entry)
            elif extension in VIDEO_EXTENSIONS:
                video_files.append(entry)
            elif extension in DOCUMENT_EXTENSIONS:
                document_files.append(entry)
            elif extension in MUSIC_EXTENSIONS:
                music_files.append(entry)
            elif extension in ARCHIVE_EXTENSIONS:
                archive_files.append(entry)
            else:
                unknown_files.append(entry)
    print(f'Image files: {image_files}')
    print(f'Video files: {video_files}')
    print(f'Document files: {document_files}')
    print(f'Music files: {music_files}')
    print(f'Archive files: {archive_files}')
    print(f'Unknown files: {unknown_files}')