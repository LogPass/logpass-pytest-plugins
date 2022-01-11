import pytest

from channels.layers import get_channel_layer
from channels.testing import (
    HttpCommunicator,
    WebsocketCommunicator,
)
from django.utils.module_loading import import_string


@pytest.fixture
async def _flush_channels(settings):
    """Flush all channels at the end of the test."""
    yield
    for alias in settings.CHANNEL_LAYERS:
        await get_channel_layer(alias).flush()


@pytest.fixture
async def websocket_communicator_factory(
    settings,
    _flush_channels,  # noqa: WPS442
):
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


@pytest.fixture
def http_communicator_factory(
    settings,
    _flush_channels,  # noqa: WPS442
):
    """``HttpCommunicator`` instances factory."""
    application = import_string(settings.ASGI_APPLICATION)

    def factory(*args, **kwargs) -> HttpCommunicator:
        """Create and register ``HttpCommunicator`` instance."""
        return HttpCommunicator(application, *args, **kwargs)

    return factory
