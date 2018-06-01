"""A script that tests grpc and protobuf through spanner.

Requests to this script validate that applications can use the spanner
grpc API to exectute a query. This API also indirectly tests protbuf.

Note: Spanner must be enabled and the database created using
create_spanner_database.sh.

"""

import traceback
from flask import Flask
from google.cloud import spanner

app = Flask(__name__)


@app.route('/')
def page_index():
  """Main test entry point."""

  r = ['Spanner client test:']

  try:
    spanner_client = spanner.Client()
    instance = spanner_client.instance('test-instance')
    database = instance.database('example-db')

    with database.snapshot() as snapshot:
      results = snapshot.execute_sql(
          "SELECT 'Success from Spanner!' as message")
      for row in results:
        r.append(row[0])

        # Stop after the first result row, because google-cloud-spanner 1.3.0
        # hasn't been updated for Python 3.7 yet, and throws a RuntimeError when
        # it hits the end:
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5282
        break

  except Exception as e:  # pylint: disable=broad-except
    r.append('Error during Spanner access: %s\n%s' % (
        repr(e), traceback.format_exc()))

  return ('\n'.join(r) + '\n'), 200, {'Content-Type': 'text/plain'}
