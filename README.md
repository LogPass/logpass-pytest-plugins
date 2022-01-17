# LogPass pytest plugins

A few pytest plugins used by LogPass.

## Installation

To use `logpass_pytest_plugins` simply install it with your package manager,
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

## Available plugins

All plugins are used by default (that's default `pytest` behaviour).
If you don't need some plugin (e.g. you don't use `djangorestframework`)
simply disable it for particular command call:

```bash
pytest -p no:rest_framework
```

or do it in `pytest.ini` (or other file with `pytest` configuration):

```ini
[pytest]
addopts = -p no:rest_framework
```

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

### `logpass_pytest_plugins.contrib.rest_framework`

Plugin that simplifies `rest_framework` views and other components testing
by providing following fixtures:

+ `api_rf` - `APIRequestFactory` instance
+ `api_client` - `APIClient` instance
