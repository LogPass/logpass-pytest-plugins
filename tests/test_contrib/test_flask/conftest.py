import pytest

from tests.logic.pytester import (
    disable_plugins,
    render_pytest_plugins,
)


@pytest.fixture
def tester(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `flask` plugin."""
    pytester.copy_example('flask/app.py')
    pytester.copy_example('flask/settings.py')
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest(
        render_pytest_plugins('logpass_pytest_plugins.contrib.flask'),
    )
    with open(pytester.path / 'pytest.ini.template') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='\n'.join([
                    'FLASK_SETTINGS_MODULE = settings',
                    'FLASK_APP = app.create_app',
                ]),
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    monkeypatch.syspath_prepend(str(pytester.path))
    monkeypatch.delenv('FLASK_APP', raising=False)
    monkeypatch.delenv('FLASK_SETTINGS_MODULE', raising=False)
    return pytester
