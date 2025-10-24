import requests
import json
import os

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")

# Get rooms
url = "https://webexapis.com/v1/rooms"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
rooms = response.json()

print("\n=== Webex Rooms ===\n")
for room in rooms.get("items", []):
    print(f"Title: {room['title']}")
    print(f"Room ID: {room['id']}")
    print(f"Type: {room['type']}")
    print("-" * 80)
