from typing import (
    AsyncGenerator,
    Callable,
)

import pytest_asyncio

from channels.layers import get_channel_layer
from channels.testing import (
    HttpCommunicator,
    WebsocketCommunicator,
)
from django.conf import Settings
from django.utils.module_loading import import_string


@pytest_asyncio.fixture
async def _flush_channels(settings: Settings) -> AsyncGenerator[None, None]:
    """Flush all channels at the end of the test."""
    yield
    for alias in settings.CHANNEL_LAYERS:
        await get_channel_layer(alias).flush()


@pytest_asyncio.fixture
async def websocket_communicator_factory(
    settings: Settings,
    _flush_channels: None,  # noqa: WPS442
) -> AsyncGenerator[Callable[[], WebsocketCommunicator], None]:
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
    settings: Settings,
    _flush_channels: None,  # noqa: WPS442
) -> Callable[[], HttpCommunicator]:
    """``HttpCommunicator`` instances factory."""
    application = import_string(settings.ASGI_APPLICATION)

    def factory(**kwargs) -> HttpCommunicator:
        """Create and register ``HttpCommunicator`` instance."""
        kwargs.setdefault('application', application)
        return HttpCommunicator(**kwargs)

    return factory
