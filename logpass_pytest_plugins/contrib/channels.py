import pytest_asyncio

from channels.layers import get_channel_layer
from channels.testing import (
    HttpCommunicator,
    WebsocketCommunicator,
)
from django.utils.module_loading import import_string


@pytest_asyncio.fixture
async def _flush_channels(settings):
    """Flush all channels at the end of the test."""
    yield
    for alias in settings.CHANNEL_LAYERS:
        await get_channel_layer(alias).flush()


@pytest_asyncio.fixture
async def websocket_communicator_factory(
    settings,
    _flush_channels,  # noqa: WPS442
):
    """Auto-disconnectable ``WebsocketCommunicator`` instances factory."""
    communicators = []
    application = import_string(settings.ASGI_APPLICATION)

    def factory(**kwargs) -> WebsocketCommunicator:
        """Create and register ``WebsocketCommunicator`` instance."""
        kwargs.setdefault('application', application)
        communicator = WebsocketCommunicator(**kwargs)
        communicators.append(communicator)
        return communicator

    yield factory

    for communicator in communicators:
        await communicator.disconnect()


@pytest_asyncio.fixture
def http_communicator_factory(
    settings,
    _flush_channels,  # noqa: WPS442
):
    """``HttpCommunicator`` instances factory."""
    application = import_string(settings.ASGI_APPLICATION)

    def factory(**kwargs) -> HttpCommunicator:
        """Create and register ``HttpCommunicator`` instance."""
        kwargs.setdefault('application', application)
        return HttpCommunicator(**kwargs)

    return factory
