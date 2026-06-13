from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def sanitize_filename(name):
    # Удаляет символы, которые запрещены в именах файлов.
    forbidden_chars = '<>:"/\\|?*'
    for char in forbidden_chars:
        name = name.replace(char, '')
    return name.strip()


def rename_mp3_files(folder_path):
    path = Path(folder_path)

    if not path.exists():
        print(f"Ошибка: Папка {folder_path} не найдена.")
        return

    print("Начало обработки файлов...\n")
    success_count = 0
    skipped_count = 0

    for file_path in path.glob("*.mp3"):
        try:
            audio = MP3(file_path, ID3=EasyID3)
            artist = audio.get('artist', [''])[0].strip()
            title = audio.get('title', [''])[0].strip()

            # Если тегов нет, пропускаем файл, чтобы не переименовать его в " - .mp3"
            if not artist or not title:
                print(f"Пропущен (нет тегов): {file_path.name}")
                skipped_count += 1
                continue
            new_name = f"{artist} - {title}"
            new_name = sanitize_filename(new_name) + ".mp3"

            new_file_path = file_path.with_name(new_name)

            if file_path == new_file_path:
                continue

            # Если файл с таким именем уже существует, добавим индекс, чтобы не перезаписать его
            counter = 1
            while new_file_path.exists():
                new_name_indexed = f"{artist} - {title} ({counter}).mp3"
                new_file_path = file_path.with_name(sanitize_filename(new_name_indexed))
                counter += 1

            file_path.rename(new_file_path)
            print(f"Переименован: {file_path.name} -> {new_file_path.name}")
            success_count += 1

        except Exception as e:
            print(f"Ошибка при обработке файла {file_path.name}: {e}")
            skipped_count += 1

    print(f"\nОбработка завершена. Переименовано: {success_count}, пропущено: {skipped_count}.")


if __name__ == "__main__":
    target_folder = "./files"
    rename_mp3_files(target_folder)