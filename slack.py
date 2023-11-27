from datetime import datetime
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from utils import get_variables, setup_logger, LOGFILE

import json

setup_logger(logfile=LOGFILE)

client = WebClient(token=get_variables('slack_bot_token'))

def convert_unix_to_datetime(unix_timestamp):
    '''
    Converts a unix timestamp to a datetime object
    '''
    dt = datetime.fromtimestamp(float(unix_timestamp))
    return dt.strftime('%Y/') + dt.strftime("%m/").lstrip("0") + dt.strftime("%d ").lstrip("0") + dt.strftime('%H:%M:%S').lstrip("0")
def get_username(user_id):
    try:
        # Fetch user information
        response = client.users_info(user=user_id)
        if response['ok']:
            # Extract the username from the response
            return response['user']['name']
        else:
            return "User not found or access denied."
    except SlackApiError as e:
        return f"Error: {e.response['error']}"

# main function
def fetch_messages_replies_reactions_from_channel(channel_name='general', private=False):
    '''
    Fetches messages and replies in a thread
    '''
    try:
        # Define lists to store messages and replies
        channel_messages = []
        channel_replies = []

        # Fetch every channel list
        if not private:
            channels = client.conversations_list()
        else:
            channels = client.conversations_list(types="private_channel")

        for channel in channels['channels']:
            # Skip channels that aren't the specified channel
            if channel['name'] != channel_name:
                continue

            channel_id = channel['id']
            print(f"Channel: {channel['name']}")

            # Fetch every post in the channel
            posts = client.conversations_history(channel=channel_id)
            for message in posts['messages']:
                messages = []

                # Skip messages that aren't messages (they're usually things like join/leave messages and thread broadcasts)
                if 'subtype' in message:
                    continue

                messages.append(message['client_msg_id']) # Message ID
                messages.append(convert_unix_to_datetime(message['ts'])) # Thread timestamp
                messages.append(get_username(message['user'])) # Username
                messages.append(message['user']) # User ID
                messages.append(message['text']) # Message text
                if 'reactions' in message:
                    for reaction in message['reactions']:
                        reaction['user_name'] = [get_username(user) for user in reaction['users']] # Add usernames to the reaction object
                    messages.append(json.dumps(message['reactions'])) # Reactions

                # Add the message to the list of messages
                channel_messages.append(messages)

                # If the message has replies
                if 'reply_count' in message:
                    replies = client.conversations_replies(channel=channel_id, ts=message['ts'])

                    replies['messages'].reverse()
                    for reply in replies['messages']:
                        if reply['client_msg_id'] == message['client_msg_id']:
                            continue
                        reply_messages = []

                        reply_messages.append(message['client_msg_id']) # Parent message ID
                        reply_messages.append(reply['client_msg_id']) # Reply message ID
                        reply_messages.append(convert_unix_to_datetime(reply['ts'])) # Thread timestamp
                        reply_messages.append(get_username(reply['user'])) # Username
                        reply_messages.append(reply['user']) # User ID
                        reply_messages.append(reply['text']) # Message text
                        if 'reactions' in reply:
                            for reaction in reply['reactions']:
                                reaction['user_name'] = [get_username(user) for user in reaction['users']] # Add usernames to the reaction object
                            reply_messages.append(json.dumps(reply['reactions'])) # Reactions

                        # Add the reply to the list of replies
                        channel_replies.append(reply_messages)

        if len(channel_messages) == 0:
            raise Exception('No messages found or channel not found')

        logger.info(f"Found {len(channel_messages)} messages and {len(channel_replies)} replies")

        channel_messages.reverse()
        channel_replies.reverse()

        return {
            'messages': channel_messages,
            'replies': channel_replies
        }
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        logger.error(f"Got an error: {e.response['error']}")
        # Also receive a corresponding status_code
        assert isinstance(e.response.status_code, int)
        logger.error(f"Received a response status_code: {e.response.status_code}")

if __name__ == "__main__":
    print(convert_unix_to_datetime(1672955785))