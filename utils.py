import os
from loguru import logger
import sys

VARIABLES = ['slack_bot_token','slcak_channel_name','google_spreadsheet_scopes','google_spreadsheet_id','google_spreadsheet_message_sheet_name','google_spreadsheet_reply_sheet_name']
VARIABLE_FILE='variables.txt'
LOGFILE='slack_automation.log'

def get_variables(variable_name):
    with open (os.path.join(os.path.dirname(__file__), VARIABLE_FILE),'r',encoding='utf-8') as f:
        variables = f.readlines()
    for variable in variables:
        if variable_name in variable:
            return variable.split('=')[1].strip()
    raise Exception(f'Variable {variable_name} not found in {VARIABLE_FILE}')
def setup_logger(logfile=""):
    logger.remove()
    if logfile != "": # If file is specified, log to file as well as console
        logger.add(logfile, rotation="100 MB",
            format='<white>{time:HH:mm:ss}</white>'
                        ' | <level>{level: <8}</level>'
                        ' | <cyan>{line}</cyan>'
                        ' - <white>{message}</white>')
    logger.add(sys.stderr,
        format='<white>{time:HH:mm:ss}</white>'
                    ' | <level>{level: <8}</level>'
                    ' | <cyan>{line}</cyan>'
                    ' - <white>{message}</white>')


if __name__ == "__main__":
    for variable in VARIABLES:
        print(f'{variable} = {get_variables(variable)}')