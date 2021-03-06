import pytest

from tests.logic.pytester import (
    disable_plugins,
    render_pytest_plugins,
)


@pytest.fixture(params=['legacy', 'auto', 'strict'])
def tester(
    request: pytest.FixtureRequest,
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> pytest.Pytester:
    """Setup ``pytester`` instance able to test `channels` plugin.

    This fixture is parametrized, so all `pytest-asycio` modes could
    be tested.
    Reference: https://github.com/pytest-dev/pytest-asyncio/#modes

    """
    pytester.copy_example('django/settings.py')
    pytester.copy_example('django/asgi.py')
    pytester.copy_example('pytest.ini.template')
    pytester.makeconftest(
        render_pytest_plugins(
            'asyncio',
            'django',
            'logpass_pytest_plugins.contrib.channels',
        ),
    )
    with open(pytester.path / 'pytest.ini.template') as pytest_ini:
        pytester.makefile(
            '.ini',
            pytest=pytest_ini.read().format(
                extra_config='\n'.join([
                    'DJANGO_SETTINGS_MODULE = settings',
                    'asyncio_mode = {0}'.format(
                        request.param,  # type: ignore[attr-defined]
                    ),
                ]),
                extra_addopts=disable_plugins('pytest-factoryboy'),
            ),
        )
    monkeypatch.syspath_prepend(str(pytester.path))
    monkeypatch.delenv('DJANGO_SETTINGS_MODULE', raising=False)
    return pytester


def test_websocket_communicator_factory(
    tester: pytest.Pytester,  # noqa: WPS442
) -> None:
    """Ensure ``websocket_communicator_factory`` creates expected objects."""
    tester.makepyfile(
        test_websocket_communicator_factory='''
        import pytest

        from channels.generic.websocket import WebsocketConsumer
        from channels.testing import WebsocketCommunicator


        @pytest.mark.asyncio
        async def test_returned_type(websocket_communicator_factory):
            assert isinstance(
                websocket_communicator_factory(path='test/communicator-type'),
                WebsocketCommunicator,
            )


        @pytest.mark.asyncio
        async def test_custom_application(websocket_communicator_factory):
            consumer = WebsocketConsumer()

            communicator = websocket_communicator_factory(
                application=consumer,
                path='test/custom-application',
            )

            assert communicator.application == consumer


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

    tests_results.assert_outcomes(passed=3)


def test_http_communicator_factory(
    tester: pytest.Pytester,  # noqa: WPS442
) -> None:
    """Ensure ``http_communicator_factory`` creates expected objects."""
    tester.makepyfile(
        test_http_communicator_factory='''
        import pytest

        from channels.generic.http import AsyncHttpConsumer
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
        async def test_custom_application(http_communicator_factory):
            consumer = AsyncHttpConsumer()

            communicator = http_communicator_factory(
                application=consumer,
                method='OPTIONS',
                path='test/custom-application',
            )

            assert communicator.application == consumer


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

    tests_results.assert_outcomes(passed=3)
