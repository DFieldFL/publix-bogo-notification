import configparser
import logging
import boto3
from bs4 import BeautifulSoup
from bogos import parse_webpage_bogos, retrieve_sales_webpage
from botocore.exceptions import ClientError


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    set_logging(config)

    logging.info('Config values:')

    keywords = []
    is_keyword_multiword = False
    url = ''
    prefix_text = ''
    postfix_text = ''
    no_bogo_text = 'No BOGOs'
    bogo_config = None

    
    if 'BOGO' not in config:
        logging.error('No BOGO config found. Exiting...')
        return
    else:
        bogo_config = config['BOGO']
        if 'keywords' not in bogo_config or 'url' not in bogo_config:
            logging.error('"keywords" or "url" was provided in the config. Exiting...')
            return
        else:
            keywords = bogo_config['keywords'].split(',')
            logging.info('keywords: ' + str(keywords))
            url = bogo_config['url']
            logging.info('url: ' + url)

    if 'keyword_multiword' in bogo_config:
        is_keyword_multiword = bogo_config.getboolean('is_keyword_multiword')
        logging.info('is_keyword_multiword: ' + str(is_keyword_multiword))

    if 'prefix_text' in bogo_config:
        prefix_text = bogo_config['prefix_text']
        logging.info('prefix_text: ' + prefix_text)

    if 'postfix_text' in bogo_config:
        postfix_text = bogo_config['postfix_text']
        logging.info('postfix_text: ' + postfix_text)

    if 'no_bogo_text' in bogo_config:
        no_bogo_text = bogo_config['no_bogo_text']
        logging.info('no_bogo_text: ' + no_bogo_text)

    bogo_items = retrieve_bogos(url)
    filtered_bogo_items = [f'{item[0]} is {item[1]}' for item in bogo_items if is_keyword_match(item[0], keywords)]
    send_bogo_notifications(filtered_bogo_items)
    logging.info(filtered_bogo_items)

def set_logging(config: configparser.ConfigParser):
    """Set the logging level based on the config otherwise default to INFO.

    Args:
        config (configparser.ConfigParser): configuration object to look for the logging level.
    """
    log_level = logging.INFO
    if 'LOGGING' in config and config['LOGGING']['LEVEL']:
        log_level = logging.getLevelName(config['LOGGING']['LEVEL'])
        logging.basicConfig(level=log_level)
        

def retrieve_bogos(bogo_url: str) -> list[(str, str)]:
    """Retrieve bogo items from the url provide.

    Args:
        bogo_url (str): url to retrieve the bogo items from

    Returns:
        list[(str, str)]: a tuple list of bogo items (<item name>, <bogo type>)
    """
    try:
        sales_content: BeautifulSoup = retrieve_sales_webpage(bogo_url)
        return parse_webpage_bogos(sales_content)
    except Exception as e:
        logging.error(e)

    return list()


def is_keyword_match(text: str, keywords: list[str]) -> bool:
    """Tells whether there is a keyword match for the given text.

    Args:
        text (str): text to match against the given keywords
        keywords (list[str]): keywords to match against the text

    Returns:
        bool: True if a keyword is in the text, otherwise False.
    """
    lower_text = text.lower()
    for s in keywords:
        if s in lower_text:
            return True

    return False


def send_bogo_notifications(bogo_items: list[str]):
    sns_resource = boto3.resource("sns")
    sms_text = '\n'.join(bogo_items)

    # TODO pass in phone number
    phone_number = '14074351722'

    try:
        response = sns_resource.meta.client.publish(
            PhoneNumber=phone_number, Message=sms_text
        )
        message_id = response["MessageId"]
        logging.info(f'Published message to {phone_number}')
    except ClientError:
        logging.exception(f"Couldn't publish message to {phone_number}")
        raise
    else:
        return message_id


if __name__ == '__main__':
    main()