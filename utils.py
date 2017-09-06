def _flatten(iterable):
    for item in iterable:
        if isinstance(item, list):
            for child in item:
                yield child
        else:
            yield item

def flatten(iterable):
    return list(_flatten(iterable))