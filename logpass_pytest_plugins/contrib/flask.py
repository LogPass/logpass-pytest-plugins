import os

from typing import (
    TYPE_CHECKING,
    Generator,
    List,
    Optional,
)

import pytest

from flask import Flask
from flask.testing import FlaskClient
from typing_extensions import Final
from werkzeug.utils import import_string

if TYPE_CHECKING:
    from _pytest.config import Config  # noqa: WPS436
    from _pytest.config.argparsing import Parser  # noqa: WPS436

SETTINGS_MODULE_ENV: Final = 'FLASK_SETTINGS_MODULE'
FLASK_APP_ENV: Final = 'FLASK_APP'
_report_headers_rows: List[str] = []


@pytest.hookimpl()  # type: ignore[misc]
def pytest_addoption(parser: 'Parser') -> None:
    """Add Flask's specific INI options."""
    parser.addini(
        SETTINGS_MODULE_ENV,
        'Flask settings module to use in tests.',
    )
    parser.addini(
        FLASK_APP_ENV,
        'Import path to Flask app or app factory.',
    )


@pytest.hookimpl()  # type: ignore[misc]
def pytest_configure(config: 'Config') -> None:
    """Use Flask's testing settings module defined in INI config."""
    settings_source = 'env'
    settings_module = config.getini(SETTINGS_MODULE_ENV)
    if settings_module:
        settings_source = 'ini'
        os.environ[SETTINGS_MODULE_ENV] = settings_module
    else:
        settings_module = os.environ[SETTINGS_MODULE_ENV]
    _report_headers_rows.append(
        'settings: "{0}" (from {1})'.format(
            settings_module,
            settings_source,
        ),
    )

    flask_app = config.getini(FLASK_APP_ENV)
    if flask_app:
        os.environ[FLASK_APP_ENV] = flask_app


@pytest.hookimpl()  # type: ignore[misc]
def pytest_report_header() -> Optional[List[str]]:
    """Print path to loaded Flask's testing settings module."""
    return ['flask: {0}'.format(', '.join(_report_headers_rows))]


@pytest.fixture
def flask_app(request: pytest.FixtureRequest) -> Generator[Flask, None, None]:
    """Flask application instance for testing purposes."""
    app_or_app_factory_import_path = os.environ.get(FLASK_APP_ENV, '')
    if not app_or_app_factory_import_path:
        raise ValueError(
            (
                'Define `flask_app` fixture or set import path to Flask app '
                + 'using "{0}" environment variable or pytest config ini.'
            ).format(FLASK_APP_ENV),
        )

    raw_app = import_string(app_or_app_factory_import_path)
    if callable(raw_app) and not isinstance(raw_app, Flask):
        app = raw_app()
    else:
        app = raw_app
    if not isinstance(app, Flask):
        raise ValueError(
            'Invalid type of Flask app - "{0}".'.format(type(app).__qualname__),
        )

    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture
def client(
    flask_app: Flask,  # noqa: WPS442
) -> Generator[FlaskClient, None, None]:
    """Flask testing HTTP client instance."""
    with flask_app.test_client() as test_client:
        yield test_client
