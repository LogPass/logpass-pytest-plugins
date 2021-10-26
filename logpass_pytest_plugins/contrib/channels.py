import pytest

from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.utils.module_loading import import_string


@pytest.fixture
async def _flush_channels(settings):
    """Flush all channels at the end of the test."""
    yield
    for alias in settings.CHANNEL_LAYERS:
        await get_channel_layer(alias).flush()


# TODO(skarzi): create fixtures for other `channels.testing` communicators
# https://github.com/LogPass/logpass_pytest_plugins/issues/1
@pytest.fixture
async def websocket_communicator_factory(
    settings,
    _flush_channels,  # noqa: WPS442
):  # noqa: WPS442
    """Auto-disconnectable ``WebsocketCommunicator`` instances factory."""
    communicators = []
    application = import_string(settings.ASGI_APPLICATION)

    def factory(*args, **kwargs) -> WebsocketCommunicator:
        """Create and register ``WebsocketCommunicator`` instance."""
        communicator = WebsocketCommunicator(
            application,
            *args,
            **kwargs,
        )
        communicators.append(communicator)
        return communicator

    yield factory

    for communicator in communicators:
        await communicator.disconnect()
