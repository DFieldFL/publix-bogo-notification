class BogoProducer:
    """Interface for BOGO producers.
    """
    def publish_bogo(self, bogo_items: list[str]) -> bool:
        raise NotImplementedError(f'publish_bogo is not implemented. Can not publish {bogo_items}');
