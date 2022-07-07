import pytest

from tests.logic.pytester import disable_plugins


def test_settings_ini(tester: pytest.Pytester) -> None:
    """Ensure ``flask_app`` config is properly populated based on ini value."""
    tester.makepyfile(
        test_settings='''
        def test_settings(flask_app):
            assert flask_app.config['ENV'] == 'test'
            assert flask_app.config['CUSTOM_VALUE'] == 123
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_settings_env(
    tester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure ``flask_app`` config is properly populated based on env value."""
    (tester.path / 'pytest.ini').unlink()
    with open(tester.path / 'pytest.ini.template') as pytest_ini:
        tester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='FLASK_APP = app.create_app',
                extra_addopts=disable_plugins(
                    'asyncio',
                    'django',
                    'pytest-factoryboy',
                ),
            ),
        )
    tester.makepyfile(
        settings_from_env="SETTINGS_SOURCE = 'env'",
    )
    monkeypatch.setenv('FLASK_SETTINGS_MODULE', 'settings_from_env')
    tester.makepyfile(
        test_settings='''
        def test_settings(flask_app):
            assert flask_app.config['SETTINGS_SOURCE'] == 'env'
            assert 'CUSTOM_VALUE' not in flask_app.config
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_client(tester: pytest.Pytester) -> None:
    """Ensure ``client`` fixtures returns expected object."""
    tester.makepyfile(
        test_client='''
        from flask.testing import FlaskClient


        def test_client(client):
            assert isinstance(client, FlaskClient)
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)
