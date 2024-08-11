import sys
import requests
from datetime import datetime, timezone
import time

# Set encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Feed URL
feed_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# Discord webhook URL
webhook_url = ""

# Store each activity
processed_ids = set()

while True:
    response = requests.get(feed_url)
    if response.status_code == 200:
        data = response.json()
        for event in data['features']:
            event_id = event['id']
            if event_id not in processed_ids:
                title = event['properties']['title']
                time_ms = event['properties']['time']
                magnitude = event['properties']['mag']

                # Convert time
                event_time = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

                # Prepare the payload
                payload = {
                    "content": f"**{title}**\n```{title}\n{magnitude} @{event_time}```"
                }

                # Send the payload to discord url
                webhook_response = requests.post(webhook_url, json=payload)
                
                if webhook_response.status_code == 204:  # Successfully sent to webhook
                    print(f"Notification sent for: {title}")
                    processed_ids.add(event_id)
                else:
                    print(f"Failed to send webhook.")

    # Check every 60 seconds
    time.sleep(60)