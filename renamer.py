import os
def rename_mp3_files(folder_path, start_number):
    # Get all MP3 files from the folder
    mp3_files = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
    mp3_files.sort()  # Sorting to maintain order

    current_number = start_number

    for file in mp3_files:
        new_name = f"bus_{current_number}.mp3"
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

        current_number += 1

# User input for start number
folder = "renamermp3"  # Change this to your actual folder path
start_number = int(input("Enter the starting number: "))

rename_mp3_files(folder, start_number)
