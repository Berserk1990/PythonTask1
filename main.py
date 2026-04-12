import sys
import shutil
import re
import unicodedata
from pathlib import Path

CATEGORIES = {
    "Images": [".jpeg", ".png", ".jpg", ".svg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".ogg", ".wav", ".amr"],
    "Archives": [".zip", ".gz", ".tar"]
}

TRANS = {
    'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh','з':'z',
    'и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p',
    'р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
    'щ':'shch','ю':'iu','я':'ia'
}

def normalize(name: str) -> str:
    result = ""

    for ch in name:
        if ch.lower() in TRANS:
            # зберігаємо регістр
            if ch.isupper():
                result += TRANS[ch.lower()].capitalize()
            else:
                result += TRANS[ch]
        elif ch.isalnum():
            result += ch
        else:
            result += "_"

    return result

def get_category(file: Path):
    ext = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def unpack_archive(file: Path, target_folder: Path):
    folder_name = normalize(file.stem)
    extract_path = target_folder / folder_name
    extract_path.mkdir(parents=True, exist_ok=True)

    try:
        shutil.unpack_archive(str(file), str(extract_path))
        print(f" Розпаковано: {file.name}")
    except shutil.ReadError:
        print(f" Не вдалося розпакувати: {file.name}")


def process_file(file: Path, base_path: Path):
    category = get_category(file)
    target_folder = base_path / category
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(file.stem) + file.suffix
    target_file = target_folder / new_name

    if category == "Archives":
        unpack_archive(file, target_folder)
        file.unlink()  # видаляємо архів
    else:
        shutil.move(str(file), str(target_file))
        print(f" {file.name} → {category}")


def sort_folder(path: Path, base_path: Path):
    for item in path.iterdir():
        if item.is_dir():
            if item.name in CATEGORIES.keys():
                continue
            sort_folder(item, base_path)
            try:
                item.rmdir()  # видаляємо пусту папку
            except OSError:
                pass
        else:
            process_file(item, base_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" Вкажи шлях до папки")
        sys.exit(1)

    folder_path = Path(sys.argv[1])
    sort_folder(folder_path, folder_path)