import os

from flask import Flask

app = Flask('test_flask_plugin')
app.config['CREATE_APP'] = False
not_flask_app = object()


def create_app() -> Flask:
    """Create `flask` app."""
    flask_app = Flask('test_flask_plugin')
    flask_app.config.from_object(os.environ['FLASK_SETTINGS_MODULE'])
    flask_app.config['CREATE_APP'] = True
    return flask_app


def create_alternative_app() -> Flask:
    """Create `flask` app."""
    flask_app = create_app()
    flask_app.config['CREATE_APP'] = False
    return flask_app
