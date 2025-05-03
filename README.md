# YouTuberEditorandUploader

This project is a complete automation pipeline for processing and uploading videos to YouTube. From basic editing to scheduling uploads, this tool is designed to streamline the workflow using Python and YouTube Data API v3.

🚀 Features
Basic Video Editing (editor.py)
Joins a simple .mp4 video file with an AI-generated .mp3 voiceover.
Final edited videos are stored in the final_videos folder.

Renaming (renamer.py)
Renames videos or audio files to follow a consistent naming format for tracking.

Automated Uploading (uploader.py)
Uploads videos to YouTube using the YouTube Data API.

Applies titles from titles.txt.
Uses a single thumbnail for all videos from the thumbnail folder.
Default description and tags can be set in the script.
Maintains upload logs in uploaded_list.txt.

Folder Structure to Track Progress

raw_videos/: Unedited source videos.
raw_mp3/: AI-generated audio files.
edited_mp3/: Edited audio if needed.
renamemp3/: For renamed audio.
final_videos/: Completed and edited videos.
uploaded_videos/: Already uploaded videos.
raw_images/: Optional - raw thumbnail images.
thumbnail/: Single thumbnail image used for uploads.

🔐 API Setup Instructions

To enable YouTube uploads:
Go to Google Cloud Console.
Create a new project.
Enable YouTube Data API v3.
Under "OAuth consent screen":
Select External.
Add scopes: https://www.googleapis.com/auth/youtube.upload
Add yourself as a Test User.
Create OAuth 2.0 Client ID:
Application type: Desktop app
Download the JSON file as client_secret.json.
On first run, authenticate your account; token.pickle will be generated for future access.

