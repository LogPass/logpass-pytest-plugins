import pytest

from rest_framework.test import (
    APIClient,
    APIRequestFactory,
)


@pytest.fixture
def api_rf():
    """``APIRequestFactory`` instance."""
    return APIRequestFactory()


@pytest.fixture
def api_client():
    """``APIClient`` instance."""
    return APIClient()
