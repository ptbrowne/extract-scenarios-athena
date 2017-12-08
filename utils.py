def _flatten(iterable):
    for item in iterable:
        if isinstance(item, list):
            for child in item:
                yield child
        else:
            yield item


def flatten(iterable):
    return list(_flatten(iterable))


def deindent(splitted_source):
  n_space = 0
  for x in splitted_source[0]:
    if x == ' ':
      n_space += 1
    else:
      break
  return map(lambda x: x[n_space:], splitted_source)


def safe_next(iterator):
  try:
    return iterator.next()
  except StopIteration:
    return None
