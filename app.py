from slack import fetch_messages_replies_reactions_from_channel
from google_sheets import build_creds, write_data
from loguru import logger

from utils import get_variables, setup_logger, LOGFILE

setup_logger(logfile=LOGFILE)

def main(channel_name, private):
    try:
        data = fetch_messages_replies_reactions_from_channel(channel_name, private)
        write_data(data)
    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    main(get_variables('slack_channel_name'), private=True)