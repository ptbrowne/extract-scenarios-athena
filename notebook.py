from json import dump, load

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

def get_cell_id(cell):
  try:
    return cell['metadata']['id']
  except KeyError:
    return None

class Notebook(dict):
  def __init__(self, *args, **kwargs):
    super(Notebook, self).__init__(*args, **kwargs)

    self.update({
     "cells": [],
     "metadata": {
      "kernelspec": {
       "display_name": "Python 2",
       "language": "python",
       "name": "python2"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 2
       },
       "file_extension": ".py",
       "mimetype": "text/x-python",
       "name": "python",
       "nbconvert_exporter": "python",
       "pygments_lexer": "ipython2",
       "version": "2.7.10"
      }
     },
     "nbformat": 4,
     "nbformat_minor": 2
    })

  def add_cell(self, source, type, id):
    splitted = map(lambda x: '%s\n' % x, source.split('\n'))
    if splitted[0] == "\n": splitted = splitted[1:]
    if splitted[-1] == "\n": splitted = splitted[:-1]
    cell = {
       "cell_type": type,
       "source": splitted,
       "metadata": { "id": id }
    }
    if id:
      cell['metadata']
    if type == 'code':
        cell['source'] = deindent(splitted)
        cell['execution_count'] = None
        cell['outputs'] = []
    self['cells'].append(cell)

  def add_code_cell(self, source, id=None):
    self.add_cell(source, 'code', id)

  def add_markdown_cell(self, source, id=None):
    self.add_cell(source, 'markdown', id)

  def write(self, filename):
    with open(filename, 'w+') as f:
      dump(self, f, indent=2)

  @staticmethod
  def open(filename):
    with open(filename) as f:
      data = load(f)
    n = Notebook()
    n.update(data)
    return n

  @staticmethod
  def merge_cells(c1, c2):
    res = []
    i1, i2 = iter(c1), iter(c2)
    cur1, cur2 = safe_next(i1), safe_next(i2)
    while cur1 is not None or cur2 is not None:
      if cur1 is None:
        res.append(cur2)
        cur2 = safe_next(i2)
      elif cur2 is None:
        res.append(cur1)
        cur1 = safe_next(i1)
      elif cur1['metadata']['id'] < cur2['metadata']['id']:
        res.append(cur1)
        cur1 = safe_next(i1)
      elif cur1['metadata']['id'] > cur2['metadata']['id']:
        res.append(cur2)
        cur2 = safe_next(i2)
      elif cur1['metadata']['id'] == cur2['metadata']['id']:
        res.append(cur1)
        cur1 = safe_next(i1)
        cur2 = safe_next(i2)
    return res

  def merge(self, other):
    self['cells'] = Notebook.merge_cells(self['cells'], other['cells'])
