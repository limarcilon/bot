import os
from flask import Flask, request, jsonify
import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]

        if event.get('type') == 'reaction_added':
            channel = event.get('item', {}).get('channel')
            timestamp = event.get('item', {}).get('ts')
            reaction = event.get('reaction')

            try:
                slack_client.reactions_add(
                    channel=channel,
                    name="thumbsup",
                    timestamp=timestamp
                )
            except SlackApiError as e:
                print(f"Error adding reaction: {e.response['error']}")

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=5000)