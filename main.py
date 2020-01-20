from parser import HocrParser
import os

DOCUMENTS_PATH = "train"

files_dict = {}
ids_folders = os.listdir(DOCUMENTS_PATH)
ids_folders = [d for d in ids_folders if os.path.isdir(d)]
for id_folder in ids_folders:
    id_folder_path = os.path.join(DOCUMENTS_PATH, id_folder)
    files = os.listdir(id_folder_path)
    hocr_file = [f for f in files if os.path.isfile(os.path.join(id_folder_path, f)) and f.endswith(".hocr")]
    try:
        hocr_file = hocr_file.pop()
        files_dict[id_folder] = hocr_file
    except Exception as e:
        continue

