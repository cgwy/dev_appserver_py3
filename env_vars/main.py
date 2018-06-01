"""A demo app for retrieving python3 runtime environment variables."""

import json
import os

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/envs')
def get_env():
  """Get the value of env var with name specified in query parameter."""
  name = request.args.get('name')
  return os.environ.get(name, '')


@app.route('/')
def all_envs():
  """Returns all env vars."""
  return json.dumps(dict(**os.environ))
