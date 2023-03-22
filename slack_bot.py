import os
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from encoder import decode_message
import requests


# Initialize the Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])


# Define the event listener for file shared
@app.event("file_shared")
def handle_file_upload(event, client):
    file_id = event["file_id"]
    try:
        response = client.files_info(file=file_id)
        file = response["file"]
        if response.data["file"]["filetype"].lower() == "gif":
            download_url = file["url_private"]
            headers = {"Authorization": "Bearer " + os.environ["SLACK_BOT_TOKEN"]}
            gif_file_response = requests.get(download_url,headers=headers)
            assert gif_file_response.status_code == 200
            data = gif_file_response.content

            message = decode_message(data)
            print(f"The hidden message was: {message}")
    except SlackApiError as e:
        print(f"Error getting file data: {e}")


if __name__ == "__main__":
    # Start the app
    handler = SocketModeHandler(app=app, app_token=os.environ["SLACK_APP_TOKEN"])
    handler.start()
