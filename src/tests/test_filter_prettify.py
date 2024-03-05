from publix_bogos.bogos import BogoItem, BogoType
from publix_bogos.filter_prettify import filter_prettify_items

effective_date = '5/3 - 5/4'
bogo_items = [BogoItem('Beer', effective_date, BogoType.BOGO,), BogoItem('Yum Beer', effective_date, BogoType.BOGO), BogoItem('Beer Yum', effective_date, BogoType.B2G1,)]

def test_items_not_filtered():
    """Assert items are not filtered."""
    items = filter_prettify_items(bogo_items, ['beer'], "pre ", " post")
    assert len(items) == 3

def test_items_are_filtered():
    """Assert items are filtered."""
    items = filter_prettify_items(bogo_items, ['nothing'], "pre ", " post")
    assert len(items) == 0


def test_items_mix_filtered():
    """Assert items are mix filtered."""
    items = filter_prettify_items(bogo_items, ['yum'], "pre ", " post")
    assert len(items) == 2


def test_items_prefix_postfix():
    """Assert items are prefixed."""
    items = filter_prettify_items(bogo_items, ['yum'], "pre ", " post")
    assert items[0].startswith('pre ')
    assert items[0].endswith(' post')
