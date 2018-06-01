"""A minimal demo app for python3 runtime."""


def app(environ, start_response):  # pylint: disable=unused-argument
  data = b"Hello, World\n"
  start_response("200 OK", [
      ("Content-Type", "text/plain"),
      ("Content-Length", str(len(data)))
  ])
  return iter([data])
