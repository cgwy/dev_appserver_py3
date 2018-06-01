"""A demo app that reports library imports for testing instance reload."""

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/libs')
def get_env():
  """Get the value of env var with name specified in query parameter."""
  name = request.args.get('name')
  try:
    lib = __import__(name)
  except ImportError:
    return 'Cannot import {}'.format(name)
  return lib.__name__
