import logging
import tweepy

from publix_bogos.producer import BogoProducer


class TwitterBogoProducer(BogoProducer):
    """Twitter BOGO Producer."""
    def __init__(self, config: dict) -> None:
        """Initialize Twitter BOGO producer.

        Args:
            config (dict): Configuration items for publishing to Twitter. Required items ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']

        Raises:
            ValueError: When a configuration item is missing from config.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        required_config = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        missing_config = [key for key in required_config if (key not in config or not config[key])]
        
        if missing_config:
            missing_keys = ', '.join(missing_config)
            raise ValueError(f'config is missing required values for [{missing_keys}]')
        
        self._config = config
    

    def _build_twitter_client(self) -> tweepy.Client:
        """Builds twitter client using configuration values.
        """
        return tweepy.Client(
        consumer_key=self._config['consumer_key'],
        consumer_secret=self._config['consumer_secret'],
        access_token=self._config['access_token'],
        access_token_secret=self._config['access_token_secret'])


    def publish_bogo(self, bogo_items: list[str]) -> bool:
        """Publish BOGO item to Twitter.

        Args:
            bogo_items (list[str]): BOGO items to publish.

        Returns:
            bool: true if BOGO items were published, otherwise false.
        """
        twitter_client = self._build_twitter_client()
        
        for bogo_text in bogo_items:
            status = twitter_client.create_tweet(text=bogo_text)
            if status is None or not status.data['id']:
                return False

        return True