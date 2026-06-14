import yaml
import os
import json
from google.cloud import pubsub_v1
from googleapiclient.discovery import build
from flask import Request

# Load config.yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize clients
youtube = build("youtube", "v3", developerKey=config["youtube_api_key"])
publisher = pubsub_v1.PublisherClient()

PROJECT_ID = os.environ.get("GCP_PROJECT", "project-df6c9b3f-5610-4979-8d5")
TOPIC_NAME = config["pubsub_topic"]
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

print(f"[INIT] Using Project ID: {PROJECT_ID}")
print(f"[INIT] Using Topic: {TOPIC_NAME}")
print(f"[INIT] Full topic path: {topic_path}")

def main(request: Request):
    print("[INFO] YouTube comment ingestion started...")
    try:
        # First get videos from channel
        search_req = youtube.search().list(
            part="id",
            channelId=config["channel_id"],
            maxResults=5,
            type="video"
        )
        search_resp = search_req.execute()
        video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
        print(f"[INFO] Found {len(video_ids)} videos.")
    except Exception as e:
        return f"Error fetching videos: {e}", 500

    published_count = 0
    for video_id in video_ids:
        try:
            request_youtube = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=config["max_results"]
            )
            response = request_youtube.execute()
            for item in response.get("items", []):
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comment_id = item["snippet"]["topLevelComment"]["id"]
                message_json = json.dumps({"id": comment_id, "comment": comment_text})
                future = publisher.publish(topic_path, message_json.encode("utf-8"))
                future.result()
                published_count += 1
        except Exception as e:
            print(f"[ERROR] video {video_id}: {e}")

    return f"Comments pushed to Pub/Sub ({published_count} messages).", 200