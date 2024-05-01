import logging

from publix_bogos.producer import BogoProducer


class LoggingBogoProducer(BogoProducer):
    """Console BOGO Producer."""
    def __init__(self, config: dict) -> None:
        """Initialize Console BOGO producer.

        Args:
            config (dict): Configuration items for publishing to console.

        Raises:
            ValueError: When a configuration item is missing from config.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._config = config


    def publish_bogo(self, bogo_items: list[str]) -> bool:
        """Publish BOGO item to Logs.

        Args:
            bogo_items (list[str]): BOGO items to publish.

        Returns:
            bool: true if BOGO items were published, otherwise false.
        """
        for bogo_text in bogo_items:
            self.logger.info(bogo_text)
        
        return True