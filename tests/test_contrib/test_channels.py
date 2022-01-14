import pytest


@pytest.fixture(params=['legacy', 'auto', 'strict'])
def tester(request, pytester, monkeypatch) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `channels` plugin.

    This fixture is parametrized, so all `pytest-asycio` modes could
    be tested.
    Reference: https://github.com/pytest-dev/pytest-asyncio/#modes

    """
    pytester.copy_example('django/settings.py')
    pytester.copy_example('django/asgi.py')
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest("pytest_plugins = ['asyncio', 'django', 'channels']")
    with open(pytester.path / 'pytest.ini.template') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='\n'.join([
                    'DJANGO_SETTINGS_MODULE = settings',
                    'asyncio_mode = {0}'.format(request.param),
                ]),
                extra_addopts=' '.join([
                    '-p no:auto_pytest_factoryboy',
                    '-p no:pytest-factoryboy',
                    '-p no:rest_framework',
                ]),
            ),
        )
    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'settings')
    monkeypatch.syspath_prepend(str(pytester.path))
    return pytester


def test_websocket_communicator_factory(tester):  # noqa: WPS442
    """Ensure ``websocket_communicator_factory`` creates expected objects."""
    tester.makepyfile(
        test_websocket_communicator_factory='''
        import pytest

        from channels.testing import WebsocketCommunicator


        @pytest.mark.asyncio
        async def test_returned_type(websocket_communicator_factory):
            assert isinstance(
                websocket_communicator_factory(path='test/communicator-type'),
                WebsocketCommunicator,
            )


        @pytest.mark.asyncio
        async def test_multiple_calls(websocket_communicator_factory):
            communicators = [
                websocket_communicator_factory(path='test/{0}'.format(counter))
                for counter in range(5)
            ]

            assert (
                [communicator.scope['path'] for communicator in communicators]
                == ['test/{0}'.format(counter) for counter in range(5)]
            )
            assert all(
                isinstance(communicator, WebsocketCommunicator)
                for communicator in communicators
            )
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=2)


def test_http_communicator_factory(tester):  # noqa: WPS442
    """Ensure ``http_communicator_factory`` creates expected objects."""
    tester.makepyfile(
        test_http_communicator_factory='''
        import pytest

        from channels.testing import HttpCommunicator


        @pytest.mark.asyncio
        async def test_returned_type(http_communicator_factory):
            assert isinstance(
                http_communicator_factory(
                    method='GET',
                    path='test/communicator-type',
                ),
                HttpCommunicator,
            )


        @pytest.mark.asyncio
        async def test_multiple_calls(http_communicator_factory):
            communicators = [
                http_communicator_factory(
                    method='POST',
                    path='test/{0}'.format(counter),
                )
                for counter in range(5)
            ]

            assert (
                [communicator.scope['path'] for communicator in communicators]
                == ['test/{0}'.format(counter) for counter in range(5)]
            )
            assert all(
                isinstance(communicator, HttpCommunicator)
                for communicator in communicators
            )
        ''',
    )

    tests_results = tester.runpytest()

    tests_results.assert_outcomes(passed=2)
