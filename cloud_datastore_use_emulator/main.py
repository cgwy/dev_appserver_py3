"""A minimal demo app for python37 using google-cloud-datastore."""

import os
from flask import Flask
from flask import request

from google.auth import credentials
from google.cloud import datastore

app = Flask(__name__)


# The kind for the new entity
ENTITY_KIND = 'Task'

# The default name of an entity
DEFAULT_NAME = 'default_name'


def _CreateDatastoreClient():
  """Create a datastore client."""
  # use dummy credential and connect to datastore emulator.
  if not os.environ.get('DATASTORE_EMULATOR_HOST'):
    raise RuntimeError(
        'Cannot find the environment variable DATASTORE_EMULATOR_HOST')
  if 'DATASTORE_DATASET' not in os.environ:
    raise RuntimeError(
        'Did not find DATASTORE_DATASET in environment variables. Cannot '
        'decide project id without it.')

  # For more information regarding AnonymousCredentials:
  # http://google-auth.readthedocs.io/en/latest/reference/google.auth.credentials.html
  return datastore.Client(credentials=credentials.AnonymousCredentials())


@app.route('/list')
def ListEntities():
  """List entities in datastore."""
  client = _CreateDatastoreClient()

  query = client.query(kind=ENTITY_KIND)
  entities = list(query.fetch())
  res = []
  for e in entities:
    res.append(e.key.path[0]['name'])
  return ' '.join(res)


@app.route('/put')
def PutEntity():
  """Put one entity into datastore."""
  client = _CreateDatastoreClient()

  name = request.args.get('name', DEFAULT_NAME)

  # The Cloud Datastore key for the new entity
  task_key = client.key(ENTITY_KIND, name)

  # Prepares the new entity
  task = datastore.Entity(key=task_key)
  task['description'] = 'From one platform'

  # Saves the entity
  client.put(task)
  return 'Successfully put entity of name: {}'.format(name)
