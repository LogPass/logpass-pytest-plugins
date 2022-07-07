def render_pytest_plugins(*plugins: str) -> str:
    """Render `pytest_plugins` list to use in `conftest.py`."""
    return 'pytest_plugins = [{0}]'.format(
        ', '.join(("'{0}'".format(plugin) for plugin in plugins)),
    )


def disable_plugins(*plugins: str) -> str:
    """Render pytest's options to disable given `plugins`."""
    return ' '.join(('-p no:{0}'.format(plugin) for plugin in plugins))
