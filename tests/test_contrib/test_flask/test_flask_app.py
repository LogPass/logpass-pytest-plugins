import pytest

from tests.logic.pytester import (
    disable_plugins,
    render_pytest_plugins,
)


def test_flask_app_ini(tester: pytest.Pytester) -> None:
    """Ensure ``flask_app`` fixture is created properly based on ini value."""
    tester.makepyfile(
        test_flask_app='''
        from flask import Flask


        def test_flask_app(flask_app):
            assert isinstance(flask_app, Flask)
            assert flask_app.config['CREATE_APP']
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_flask_app_env(
    tester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure ``flask_app`` fixture is created properly based on env value."""
    (tester.path / 'pytest.ini').unlink()
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='FLASK_SETTINGS_MODULE = settings',
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    monkeypatch.setenv('FLASK_APP', 'app.create_alternative_app')
    tester.makepyfile(
        test_flask_app='''
        from flask import Flask


        def test_flask_app(flask_app):
            assert isinstance(flask_app, Flask)
            assert not flask_app.config['CREATE_APP']
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_flask_app_direct(tester: pytest.Pytester) -> None:
    """Ensure ``flask_app`` fixture is created properly when directly set."""
    (tester.path / 'pytest.ini').unlink()
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='\n'.join([
                    'FLASK_SETTINGS_MODULE = settings',
                    'FLASK_APP = app.app',
                ]),
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    tester.makepyfile(
        test_flask_app='''
        from flask import Flask


        def test_flask_app(flask_app):
            assert isinstance(flask_app, Flask)
            assert not flask_app.config['CREATE_APP']
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_flask_app_invalid_type(tester: pytest.Pytester) -> None:
    """Ensure ``ValueError`` is raised when flask app has invalid type."""
    (tester.path / 'pytest.ini').unlink()
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='\n'.join([
                    'FLASK_SETTINGS_MODULE = settings',
                    'FLASK_APP = app.not_flask_app',
                ]),
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    tester.makepyfile(test_flask_app='def test_flask_app(flask_app): ...')

    tests_results = tester.runpytest()

    tests_results.stdout.fnmatch_lines(
        '*Invalid type of Flask app - "object"*',
    )


def test_flask_app_conftest(tester: pytest.Pytester) -> None:
    """Ensure ``flask_app`` fixture is taken from conftest when defined."""
    (tester.path / 'conftest.py').unlink()
    (tester.path / 'pytest.ini').unlink()
    conftest_content = '\n'.join([
        'import pytest',
        'from flask import Flask',
        render_pytest_plugins(
            'django',
            'logpass_pytest_plugins.contrib.flask',
        ),
        '@pytest.fixture',
        'def flask_app():',
        "    app = Flask('test_flask_plugin')",
        "    app.config['DEFINED_IN_FIXTURE'] = True",
        '    return app',
    ])
    tester.makeconftest(conftest_content)
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='FLASK_SETTINGS_MODULE = settings',
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    tester.makepyfile(
        test_flask_app='''
        from flask import Flask


        def test_flask_app(flask_app):
            assert isinstance(flask_app, Flask)
            assert flask_app.config['DEFINED_IN_FIXTURE']
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_flask_app_not_set(tester: pytest.Pytester) -> None:
    """Ensure ``ValueError`` is raised when flask app not set."""
    (tester.path / 'pytest.ini').unlink()
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='FLASK_SETTINGS_MODULE = settings',
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    tester.makepyfile(test_flask_app='def test_flask_app(flask_app): ...')

    tests_results = tester.runpytest()

    tests_results.stdout.fnmatch_lines(
        '*Define `flask_app` fixture or set import path*',
    )
