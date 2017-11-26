from json import dump

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

  def add_cell(self, source, type):
    splitted = map(lambda x: '%s\n' % x, source.split('\n'))
    if splitted[0] == "\n": splitted = splitted[1:]
    if splitted[-1] == "\n": splitted = splitted[:-1]
    cell = {
       "cell_type": type,
       "source": splitted,
       "metadata": {}
    }
    if type == 'code':
        cell['execution_count'] = None
        cell['outputs'] = []
    self['cells'].append(cell)

  def add_code_cell(self, source):
    self.add_cell(source, 'code')

  def add_markdown_cell(self, source):
    self.add_cell(source, 'markdown')

  def write(self, filename):
    with open(filename, 'w+') as f:
      dump(self, f, indent=2)
