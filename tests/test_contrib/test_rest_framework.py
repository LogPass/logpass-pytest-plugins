import pytest


@pytest.fixture
def tester(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `rest_framework` plugin."""
    pytester.copy_example('django/settings.py')
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest("pytest_plugins = ['django', 'rest_framework']")
    with open(pytester.path / 'pytest.ini.template') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='DJANGO_SETTINGS_MODULE = settings',
                extra_addopts=' '.join([
                    '-p no:asyncio',
                    '-p no:auto_pytest_factoryboy',
                    '-p no:channels',
                    '-p no:pytest-factoryboy',
                ]),
            ),
        )
    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'settings')
    monkeypatch.syspath_prepend(str(pytester.path))
    return pytester


def test_api_client(tester: pytest.Pytester) -> None:  # noqa: WPS442
    """Ensure ``api_client`` fixtures returns expected object."""
    tester.makepyfile(
        test_api_client='''
        from rest_framework.test import APIClient


        def test_api_client(api_client):
            assert isinstance(api_client, APIClient)
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)


def test_api_rf(tester: pytest.Pytester) -> None:  # noqa: WPS442
    """Ensure ``api_rf`` fixtures returns expected object."""
    tester.makepyfile(
        test_api_rf='''
        from rest_framework.test import APIRequestFactory


        def test_api_rf(api_rf):
            assert isinstance(api_rf, APIRequestFactory)
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=1)
