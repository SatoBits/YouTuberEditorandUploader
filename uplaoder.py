import os
import pickle
import shutil
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Configurations
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_FOLDER = "final_videos/"
THUMBNAIL_FOLDER = "thumbnails/"
UPLOADED_VIDEO_FOLDER = "uploaded_videos/"
TITLE_FILE = "titles.txt"
SCHEDULE_FILE = "schedule.txt"
UPLOAD_LOG_FILE = "uploaded_log.txt"
UPLOAD_LIMIT = 1  # For testing

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(credentials, token)
    print("✅ Authentication Successful! Token saved.")

def load_credentials():
    with open("token.pickle", "rb") as token:
        return pickle.load(token)

def get_scheduled_videos():
    scheduled_videos = []
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            parts = line.strip().split(" - ")
            if len(parts) == 2:
                filename, schedule_time = parts
                dt = datetime.strptime(schedule_time, "%d %B %Y, %H:%M IST")
                publish_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                scheduled_videos.append((filename, publish_time))
    return scheduled_videos

def get_titles():
    with open(TITLE_FILE, "r", encoding="utf-8") as f:
        return [title.strip() for title in f.readlines()]

def get_fixed_thumbnail():
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, "thumbnail.jpg")
    if os.path.exists(thumbnail_path):
        return thumbnail_path
    else:
        print("⚠️ thumbnail.jpg not found!")
        return None

def load_uploaded_log():
    if not os.path.exists(UPLOAD_LOG_FILE):
        return set()
    with open(UPLOAD_LOG_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def save_uploaded_log(video_filename):
    with open(UPLOAD_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{video_filename}\n")

def upload_video(video_path, title, thumbnail_path, publish_time):
    credentials = load_credentials()
    youtube = build("youtube", "v3", credentials=credentials)

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": """About Pickypie:

Where kids can be happy and smart!

At Pickypie, our goal is to help make learning a fun and enjoyable experience for kids by creating beautiful 3D animation, educational lyrics, and toe-tapping music.

Kids will laugh, dance, sing, and play along with our videos, learning letters, numbers, animal sounds, colors, and much, much more while simply enjoying our friendly characters and fun stories.

We also make life easier for parents who want to keep their kids happily entertained, giving you the peace of mind that your children are receiving quality educational content. Our videos also give you an opportunity to teach and play with your children as you both watch!
""",
                "categoryId": "10",
                "tags": [
                    "nursery rhymes", "kids songs", "baby songs", "preschool learning", "wheels on the bus",
                    "baby shark song", "toddler music", "sing along", "educational videos", "phonics songs", "lullabies",
                    "learning songs for kids"
                ]
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_time,
            },
        },
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⏫ Upload progress: {int(status.progress() * 100)}%")

    video_id = response['id']
    print(f"✅ Video uploaded: {video_id}")

    # ✅ Upload Thumbnail
    if thumbnail_path:
        try:
            thumb_request = youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            thumb_request.execute()
            print("✅ Thumbnail uploaded!")
        except Exception as e:
            print(f"⚠️ Thumbnail upload failed: {e}")
    else:
        print("⚠️ No thumbnail provided.")

    media.stream().close()

    try:
        shutil.move(video_path, os.path.join(UPLOADED_VIDEO_FOLDER, os.path.basename(video_path)))
        print("📂 Moved video to uploaded folder.")
    except Exception as e:
        print(f"⚠️ Could not move video file: {e}")

# Run authentication if needed
if not os.path.exists("token.pickle"):
    authenticate()

scheduled_videos = get_scheduled_videos()
titles = get_titles()
uploaded_log = load_uploaded_log()
thumbnail = get_fixed_thumbnail()

uploaded_count = 0
for i, (video_filename, publish_time) in enumerate(scheduled_videos):
    if uploaded_count >= UPLOAD_LIMIT:
        print(f"🛑 Reached upload limit of {UPLOAD_LIMIT}.")
        break

    if video_filename in uploaded_log:
        print(f"⏭️ Skipping already uploaded video: {video_filename}")
        continue

    video_path = os.path.join(VIDEO_FOLDER, video_filename)

    if os.path.exists(video_path):
        title = titles[i] if i < len(titles) else "Untitled Video"
        print(f"🎬 Uploading: {video_filename} with title: {title}")
        upload_video(video_path, title, thumbnail, publish_time)
        save_uploaded_log(video_filename)
        uploaded_count += 1
    else:
        print(f"❌ Video file {video_filename} not found!")
