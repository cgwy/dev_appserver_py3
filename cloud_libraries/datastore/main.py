"""A minimal demo app for python37 using google-cloud-datastore talking to production backend."""

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
  return datastore.Client()


def _CheckEnv():
  if os.environ.get('DATASTORE_EMULATOR_HOST', ''):
    exit('Should not have DATASTORE_EMULATOR_HOST when talking to real datastore')


@app.route('/list')
def ListEntities():
  """List entities in datastore."""
  _CheckEnv()
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
  _CheckEnv()
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
