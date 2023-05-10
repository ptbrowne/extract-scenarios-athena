from json import dump, load
from itertools import chain
from contextlib import contextmanager
from utils import deindent, safe_next

def get_cell_id(cell):
  try:
    return cell['metadata']['id']
  except KeyError:
    return None

def get_group(cell):
  return get_cell_id(cell).split('.')[0]

class Notebook(dict):
  def __init__(self, *args, **kwargs):
    super(Notebook, self).__init__(*args, **kwargs)

    self.section = ''
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
    splitted = ['%s\n' % x for x in source.split('\n')]
    if splitted[0] == "\n": splitted = splitted[1:]
    if splitted[-1] == "\n": splitted = splitted[:-1]
    cell = {
      "cell_type": type,
      "source": splitted,
      "metadata": {
        "id": '%s.%s' % (self.section, id) if len(self.section) else id,
        "hide_input": True,
        "init_cell": True
      }
    }
    if type == 'code':
        cell['source'] = deindent(splitted)
        cell['execution_count'] = None
        cell['outputs'] = []
    self['cells'].append(cell)

  def add_code_cell(self, source, id=None):
    self.add_cell(source, 'code', id)

  def add_markdown_cell(self, source, id=None):
    self.add_cell(source, 'markdown', id)

  @contextmanager
  def subsection(self, section_name):
    old = self.section
    self.section = '%s.%s' % (self.section, section_name) if len(self.section) else section_name 
    yield
    self.section = old

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

    groups = [get_group(c) for c in chain(c1, c2)]
    groups = list(set(groups))

    groups = sorted(groups)

    for group in groups:

      def iter_on(cells, group):
        return (c for c in cells if get_group(c) == group)

      i1, i2 = iter_on(c1, group), iter_on(c2, group)
      cur1, cur2 = safe_next(i1), safe_next(i2)

      while cur1 is not None or cur2 is not None:
        if cur1 is None:
          # print '+ ', get_cell_id(cur2)
          res.append(cur2)
          cur2 = safe_next(i2)
        elif cur2 is None:
          # print '  ', get_cell_id(cur1)
          res.append(cur1)
          cur1 = safe_next(i1)
        elif get_cell_id(cur1) < get_cell_id(cur2):
          # print '  ', get_cell_id(cur1)
          res.append(cur1)
          cur1 = safe_next(i1)
        elif get_cell_id(cur1) > get_cell_id(cur2):
          # print '+ ', get_cell_id(cur2)
          res.append(cur2)
          cur2 = safe_next(i2)
        elif get_cell_id(cur1) == get_cell_id(cur2):
          # print '  ', cur1['metadata']['id']
          res.append(cur1)
          cur1 = safe_next(i1)
          cur2 = safe_next(i2)
    return res

  def merge(self, other):
    self['cells'] = Notebook.merge_cells(self['cells'], other['cells'])
