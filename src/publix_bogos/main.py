import configparser
import logging
from bs4 import BeautifulSoup
from bogos import BogoItem, parse_webpage_bogos, retrieve_sales_webpage

from publix_bogos.console import LoggingBogoProducer
from publix_bogos.filter_prettify import filter_prettify_items
from publix_bogos.producer import BogoProducer
from publix_bogos.tweeter import TwitterBogoProducer

logger = logging.getLogger(__name__)


def main():
    # RawConfigParser is needed because things like Twitter API keys have characters like '%' in them
    config = configparser.RawConfigParser()
    config.read('config.ini')

    set_logging(config)

    logger.info('Config values:')

    keywords = []
    url = ''
    prefix_text = ''
    postfix_text = ''
    no_bogo_text = 'No BOGOs'
    bogo_config = None


    if 'BOGO' not in config:
        logger.error('No BOGO config found. Exiting...')
        return
    else:
        bogo_config = config['BOGO']
        if 'keywords' not in bogo_config or 'url' not in bogo_config:
            logger.error('"keywords" or "url" was provided in the config. Exiting...')
            return
        else:
            keywords = bogo_config['keywords'].split(',')
            logger.info('keywords: ' + str(keywords))
            url = bogo_config['url']
            logger.info('url: ' + url)

    if 'prefix_text' in bogo_config:
        prefix_text = bogo_config['prefix_text']
        logger.info('prefix_text: ' + prefix_text)

    if 'postfix_text' in bogo_config:
        postfix_text = bogo_config['postfix_text']
        logger.info('postfix_text: ' + postfix_text)

    if 'no_bogo_text' in bogo_config:
        no_bogo_text = bogo_config['no_bogo_text']
        logger.info('no_bogo_text: ' + no_bogo_text)

    bogo_items = retrieve_bogos(url)
    filtered_prettified_bogo_items = filter_prettify_items(bogo_items, keywords, prefix_text, postfix_text)

    # send pretty text to destination
    publish_bogo_items(filtered_prettified_bogo_items, config)


def set_logging(config: configparser.RawConfigParser):
    """Set the logging level based on the config otherwise default to INFO.

    Args:
        config (configparser.RawConfigParser): configuration object to look for the logging level.
    """
    log_level = logging.INFO
    if 'logging' in config and config['logging']['level']:
        log_level_mapping = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARNING,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            }
        log_level = log_level_mapping.get(config['logging']['level'], logging.INFO)

    logging.basicConfig(level=log_level)


def retrieve_bogos(bogo_url: str) -> list[BogoItem]:
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
        logger.error(e)

    return list()


def publish_bogo_items(bogo_items: list[str], config: configparser.RawConfigParser):
    """Publish bogo items to configured producers (config['BOGO']['producers']).

    Args:
        bogo_items (list[str]): BOGO items to publish.
        config (configparser.RawConfigParser): Configuration for where to publish BOGOs.
    """
    if 'producers' not in config['BOGO'] or not config['BOGO']['producers']:
        logger.warn('No producers are configured for publishing BOGOs.')
        return

    for producer_type in config['BOGO']['producers'].split(','):
        producer: BogoProducer = build_producer(producer_type, config[producer_type])
        producer.publish_bogo(bogo_items)



def build_producer(producer_type, config: configparser.RawConfigParser) -> BogoProducer:
    """Build the appropriate producer.

    Args:
        producer_type (_type_): Producer type.
        config (configparser.RawConfigParser): Configuration to pass to the producer.

    Returns:
        BogoProducer: Built producer using the type and the config.
    """
    config_dict = dict(config)
    match producer_type:
        case 'twitter_producer':
            return TwitterBogoProducer(config_dict)
        case 'logging_producer':
            return LoggingBogoProducer(config_dict)
        case _:
            raise LookupError(f'No producer is found for type "{producer_type}"')


if __name__ == '__main__':
    main()
