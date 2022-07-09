# LogPass pytest plugins

A few pytest plugins used by LogPass.

## Installation

To use `logpass_pytest_plugins` install it with your package manager,
e.g. via pip:

```bash
pip install logpass_pytest_plugins
```

To install plugin with all its dependencies use one of following extras:

+ `auto_pytest_factoryboy`
+ `channels`
+ `rest_framework`

For instance, to install `channels` and `rest_framework` plugins with all
dependencies:

```bash
pip install logpass_pytest_plugins[channels,rest_framework]
```

And finally add plugin import path to [pytest_plugins][] in your root
`conftest.py` file, e.g. to use `channels` and `rest_framework` plugins:

```python
# root `conftest.py`
pytest_plugins = (
    'logpass_pytest_plugins.contrib.channels',
    'logpass_pytest_plugins.contrib.rest_framework',
)
```

## Available plugins

NOTE: None plugin is **not** used by default - you need to enable them via
[pytest_plugins]

### `logpass_pytest_plugins.contrib.auto_pytest_factoryboy`

Plugin that automatically registers `factory_boy` factories to
`pytest-factoryboy`, so factories and models instances will be available
as pytest fixtures.

#### Configuration

Following INI options can be used to configure `auto_pytest_factoryboy` plugin:

+ `auto_pytest_factoryboy_root_dir` - directory where factories declarations
  searching starts (defaults to `.` - pytest config path)
+ `auto_pytest_factoryboy_globs` - list of `glob` patterns used to find files
  with `factoryboy` factories declarations starting from the
  `auto_pytest_factoryboy_root_dir` directory (defaults to `**/factories*.py`)

### `logpass_pytest_plugins.contrib.channels`

Plugin that simplifies `channels` consumers testing by providing following
fixtures:

+ `websocket_commmunicator_factory` - factory of `WebSocketCommunicator`
  instances, that will automatically disconnect at the end of a test.
  Using this fixture also automatically flush all used channel layers
+ `http_commmunicator_factory` - factory of `HttpCommunicator`
  instances. Using this fixture also automatically flush all used
  channel layers

### `logpass_pytest_plugins.contrib.flask`

Plugin that simplifies `flask` views and other components testing
by providing following fixtures:

+ `flask_app` - `Flask` app instance
+ `client` - `FlaskClient` instance to use in tests

Following INI options can be used to configure `flask` plugin:

+ `FLASK_SETTINGS_MODULE` - import path to settings module when using
  flask's config from object. Overrides `FLASK_SETTINGS_MODULE` environment
  variable.
+ `FLASK_APP` - import path to flask app factory or flask app instance.
  Overrides `FLASK_APP` environment variable.

To use `flask` plugin you need to do one of following:

+ set `FLASK_APP` INI option
+ set `FLASK_APP` environment variable
+ define `flask_app` function-scoped fixture in root `conftest.py`

### `logpass_pytest_plugins.contrib.rest_framework`

Plugin that simplifies `rest_framework` views and other components testing
by providing following fixtures:

+ `api_rf` - `APIRequestFactory` instance
+ `api_client` - `APIClient` instance

[pytest_plugins]: https://docs.pytest.org/en/7.1.x/how-to/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file "`pytest_plugins`"
