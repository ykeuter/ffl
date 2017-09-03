#!venv/bin/python
from werkzeug.contrib.profiler import ProfilerMiddleware
from ffl import app

app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(debug=True)

