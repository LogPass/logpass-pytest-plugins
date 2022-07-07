from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from rest_framework.test import (
        APIClient,
        APIRequestFactory,
    )


@pytest.fixture
def api_rf() -> 'APIRequestFactory':
    """``APIRequestFactory`` instance."""
    from rest_framework.test import APIRequestFactory  # noqa: WPS433, WPS442

    return APIRequestFactory()


@pytest.fixture
def api_client() -> 'APIClient':
    """``APIClient`` instance."""
    from rest_framework.test import APIClient  # noqa: WPS433, WPS442

    return APIClient()
