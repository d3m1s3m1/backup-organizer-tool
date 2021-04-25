from config import *
from PIL import Image
import datetime
import os
import shutil
import zipfile
import tkinter as tk


def copy_file_to_folder(start_file_path, to_file_path):
    if not os.path.exists(to_file_path):
        print(f"NOW COPYING {start_file_path}")
        shutil.copy2(start_file_path, to_file_path)
    else:
        print(f"FILE ALREADY EXISTS! {start_file_path}")


def move_file_to_folder(start_file_path, to_file_path):
    if start_file_path == to_file_path:
        return
    if os.path.exists(to_file_path):
        os.remove(to_file_path)
        print(f"DELETED DUPLICATE! {to_file_path}")
    print(f"MOVING FILE {os.path.basename(start_file_path)}")
    os.rename(start_file_path, to_file_path)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def get_creation_date_of_photo(photo_path):
    file_name = os.path.basename(photo_path)
    file_name = file_name[:len(file_name) - len(os.path.splitext(file_name)[1])]
    try:
        full_date = Image.open(photo_path).getexif()[36867].split(" ")[0]
        year = full_date.split(":")[0]
        month = full_date.split(":")[1]
        return str(year), int(month)
    except Exception:
        try:
            FILE_DATE = datetime.datetime.strptime(file_name, "%Y%m%d_%H%M%S")
        except:
            FILE_UNIX = os.path.getmtime(photo_path)
            FILE_DATE = datetime.datetime.fromtimestamp(FILE_UNIX)
        finally:
            year = FILE_DATE.year
            month = FILE_DATE.month
    return str(year), int(month)


def extract_all_from(folder_path):
    try:
        with zipfile.ZipFile(folder_path, 'r') as zip_ref:
            EXTRACTION_FOLDER = os.path.join(ZIP_CACHE_FOLDER, os.path.basename(folder_path))
            if not os.path.exists(EXTRACTION_FOLDER):
                zip_ref.extractall(EXTRACTION_FOLDER)
            else:
                print(f"ALREADY EXTRACTED! {EXTRACTION_FOLDER}")
    except zipfile.BadZipFile:
        print(f"ERROR WHILST EXTRACTING {folder_path}")


def backup(mode="move"):
    assert mode == "move" or mode == "copy"
    print(f"STARTING BACKUP WITH MODE: {mode.upper()}")
    for FILE_FOLDER in FOLDER_WALK:
        FILES = FILE_FOLDER[2]
        FILES_PATH = FILE_FOLDER[0]

        for file in FILES:
            MY_FILE_PATH = os.path.join(FILES_PATH, file)
            FILE_EXTENSION = os.path.splitext(MY_FILE_PATH)[1]

            if FILE_EXTENSION.lower() not in BACKUP_EXTENSIONS:
                print(f"DISREGARDED EXTENSION {FILE_EXTENSION}")
                continue

            FILE_YEAR, FILE_MONTH = get_creation_date_of_photo(MY_FILE_PATH)
            FILE_MONTH = f"{FILE_MONTH} - {MONTHS[FILE_MONTH - 1]}"

            # CREATE YEAR FOLDER
            create_folder(os.path.join(MAIN_BACKUP_FOLDER, FILE_YEAR))

            # CREATE MONTH FOLDER
            MOVE_FILE_TO_PATH = os.path.join(MAIN_BACKUP_FOLDER, FILE_YEAR, FILE_MONTH)
            create_folder(MOVE_FILE_TO_PATH)
            MOVE_FILE_TO_PATH = os.path.join(MOVE_FILE_TO_PATH, file)

            # COPY FILE TO DEDICATED FOLDER
            if mode == "move":
                move_file_to_folder(MY_FILE_PATH, MOVE_FILE_TO_PATH)
            elif mode == "copy":
                copy_file_to_folder(MY_FILE_PATH, MOVE_FILE_TO_PATH)


def backup_zip():
    for FILE_FOLDER in FOLDER_WALK:
        FILES = FILE_FOLDER[2]
        FILES_PATH = FILE_FOLDER[0]
        for file in FILES:
            MY_FILE_PATH = os.path.join(FILES_PATH, file)
            FILE_EXTENSION = os.path.splitext(MY_FILE_PATH)[1]

            if FILE_EXTENSION.lower() != ".zip":
                # print(f"DISREGARDED EXTENSION {FILE_EXTENSION}")
                continue
            print(f"Extracting {MY_FILE_PATH}")
            extract_all_from(MY_FILE_PATH)


FOLDER_TO_BACKUP = r"G:\Note5"
FOLDER_WALK = os.walk(FOLDER_TO_BACKUP)
ZIP_CACHE_FOLDER = os.path.join(MAIN_BACKUP_FOLDER, "ZIPCACHE")
create_folder(ZIP_CACHE_FOLDER)


class Application(tk.Frame):
    def __init__(self, master=None):
        v = tk.IntVar()
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=1)
        self.master.maxsize(320, 200)

        tk.Radiobutton(root,
                       text="Move",
                       padx=5,
                       variable=v,
                       value=1).pack(anchor=tk.W)

        tk.Radiobutton(root,
                       text="Copy",
                       padx=5,
                       variable=v,
                       value=2).pack(anchor=tk.W)

        start_button = tk.Button(root,
                                 text="Start Backup",
                                 justify=tk.CENTER,
                                 width=100)
        start_button.pack()

        tk.Label(root, text="Folder to Backup").place(x=5, y=5)
        tk.Entry(root, width=50).place(x=5, y=30)

        tk.Label(root, text="Backup Folder").place(x=5, y=55)
        tk.Entry(root, width=50).place(x=5, y=80)


root = tk.Tk()
root.geometry("320x200")
root.title("Backupinator v.0")
app = Application(master=root)

if __name__ == "__main__":
    app.mainloop()
    # backup(mode="move")
