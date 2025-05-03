import os
import random
import shutil
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip


def create_video(mp3_file, mp4_folder, output_folder, edited_mp3_folder):
    # MP4 Files Randomly Pick
    mp4_files = [os.path.join(mp4_folder, f) for f in os.listdir(mp4_folder) if f.endswith('.mp4')]
    random.shuffle(mp4_files)

    if not mp4_files:
        print("❌ No MP4 files found!")
        return

    # Load audio file
    audio = AudioFileClip(mp3_file)
    audio_duration = audio.duration

    clips = []
    total_duration = 0

    for file in mp4_files:
        if total_duration >= audio_duration:
            break
        clip = VideoFileClip(file)
        clips.append(clip)
        total_duration += clip.duration

    # Adjust last clip to match audio duration
    if total_duration > audio_duration:
        excess_duration = total_duration - audio_duration
        clips[-1] = clips[-1].subclipped(0, clips[-1].duration - excess_duration)

    # Merge clips
    final_video = concatenate_videoclips(clips, method="compose").with_audio(audio).with_duration(audio.duration)
    final_video = final_video.resized((1920, 1080))

    # Output file path
    output_file = os.path.join(output_folder, os.path.basename(mp3_file).replace(".mp3", ".mp4"))

    # Fast Export
    final_video.write_videofile(
        output_file,
        codec="h264_nvenc",
        preset="p4",
        bitrate="10M",
        fps=30,
        threads=8  # Optimize for available CPU threads
    )

    print(f"✅ Exported: {output_file}")

    # Move processed MP3 file to edited_mp3 folder
    os.makedirs(edited_mp3_folder, exist_ok=True)
    shutil.move(mp3_file, os.path.join(edited_mp3_folder, os.path.basename(mp3_file)))
    print(f"📂 Moved MP3 to {edited_mp3_folder}")


# Example Usage
mp3_folder = r"C:\Users\kuwer\PycharmProjects\PythonProject\raw_mp3"
mp4_folder = r"C:\Users\kuwer\PycharmProjects\PythonProject\raw_videos"
output_folder = r"C:\Users\kuwer\PycharmProjects\PythonProject\final_videos"
edited_mp3_folder = r"C:\Users\kuwer\PycharmProjects\PythonProject\edited_mp3"

for mp3 in os.listdir(mp3_folder):
    if mp3.endswith(".mp3"):
        create_video(os.path.join(mp3_folder, mp3), mp4_folder, output_folder, edited_mp3_folder)