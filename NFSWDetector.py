import requests
import opennsfw2 as n2
import json
import os

# Function to download video from URL
def download_video(url, save_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

# URL of the video
video_url = "https://shramin.blob.core.windows.net/files/video/1632639355329-9fd3edbe-aaf3-484d-9f92-1a405d0c6770-videoResume.mp4"

# Local path to save the video
video_path = "video.mp4"

# Download the video
download_video(video_url, video_path)

# Return two lists giving the elapsed time in seconds and the NSFW probability of each frame.
elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(video_path)

# Find the highest NSFW probability
highest_nsfw_probability = max(nsfw_probabilities)

# Define the threshold for NSFW classification
threshold = 0.1

# Determine the label based on the threshold
label = "Not Safe For Work" if highest_nsfw_probability > threshold else "Safe For Work"

# Create a dictionary for the result
result = {
    "score": highest_nsfw_probability,
    "label": label
}

# Convert the result to JSON format
json_result = json.dumps(result, indent=4)

# Print only the JSON result
print(json_result)

# Delete the temporary video file
os.remove(video_path)

