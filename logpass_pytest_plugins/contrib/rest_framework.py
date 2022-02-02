import pytest


@pytest.fixture
def api_rf():
    """``APIRequestFactory`` instance."""
    from rest_framework.test import APIRequestFactory  # noqa: WPS433

    return APIRequestFactory()


@pytest.fixture
def api_client():
    """``APIClient`` instance."""
    from rest_framework.test import APIClient  # noqa: WPS433

    return APIClient()
