import pytest


@pytest.fixture
def tester(pytester, monkeypatch) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `channels` plugin."""
    pytester.copy_example('django/settings.py')
    pytester.copy_example('django/asgi.py')
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest("pytest_plugins = ['asyncio', 'django', 'channels']")
    with open((pytester.path / 'pytest.ini.template'), mode='r') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='DJANGO_SETTINGS_MODULE = settings',
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
