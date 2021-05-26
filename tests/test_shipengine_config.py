"""Testing the ShipEngineConfig object."""
import pytest

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import InvalidFieldValueError, ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.models.enums import Endpoints
from shipengine_sdk.util import api_key_validation_error_assertions


def config_with_no_api_key() -> ShipEngineConfig:
    """Return an error from no API Key."""
    return ShipEngineConfig(dict(retries=2))


def config_with_empty_api_key() -> ShipEngineConfig:
    """Return an error from empty API Key."""
    return ShipEngineConfig(dict(api_key=""))


def config_with_whitespace_in_api_key() -> ShipEngineConfig:
    """Return an error from whitespace in API Key."""
    return ShipEngineConfig(dict(api_key=" "))


def set_config_timeout(timeout: int) -> ShipEngineConfig:
    """
    Return an error from an invalid timeout value being passed in or
    returns the successfully created `ShipEngineConfig` object if valid
    configuration values are passed in.

    :param int timeout: The timeout to be passed into the `ShipEngineConfig` object.
    :returns: :class:`ShipEngineConfig`: Global configuration object for the ShipEngine SDK.
    :raises: :class:`InvalidFieldValueError`: If invalid value is passed into `ShipEngineConfig`
    object at instantiation.
    """
    return ShipEngineConfig(dict(api_key="baz", timeout=timeout))


def set_config_retries(retries: int) -> ShipEngineConfig:
    """
    Return a ShipEngineConfig object with the set retries and
    API Key, where the rest of the configuration values are
    the default values.

    :param int retries: The retries to be passed into the `ShipEngineConfig` object.
    :returns: :class:`ShipEngineConfig`: Global configuration object for the ShipEngine SDK.
    :raises: :class:`InvalidFieldValueError`: If invalid value is passed into `ShipEngineConfig`
    object at instantiation.
    """
    return ShipEngineConfig(dict(api_key="baz", retries=retries))


def complete_valid_config() -> ShipEngineConfig:
    """
    Return a `ShipEngineConfig` object that has valid custom
    values passed in.
    """
    return ShipEngineConfig(
        dict(
            api_key="baz",
            base_uri=Endpoints.TEST_RPC_URL.value,
            page_size=50,
            retries=2,
            timeout=10,
        )
    )


class TestShipEngineConfig:
    def test_valid_custom_config(self):
        """
        Test case where a config object has been passed custom
        valid values for each attribute.
        """
        valid_config: ShipEngineConfig = complete_valid_config()
        assert valid_config.api_key == "baz"
        assert valid_config.base_uri is Endpoints.TEST_RPC_URL.value
        assert valid_config.page_size == 50
        assert valid_config.retries == 2
        assert valid_config.timeout == 10

    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation"""
        try:
            config_with_no_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_no_api_key()

    def test_empty_api_key_provided(self) -> None:
        """DX-1441 - Empty API Key at instantiation."""
        try:
            config_with_empty_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_empty_api_key()

    def test_valid_retries(self):
        """Test case where a valid value is passed in for the retries."""
        retries = 2
        valid_retries = set_config_retries(retries)
        assert valid_retries.api_key == "baz"
        assert valid_retries.retries == retries

    def test_invalid_retries_provided(self):
        """DX-1442 - Invalid retries at instantiation."""
        retries = -3
        try:
            set_config_retries(retries)
        except InvalidFieldValueError as e:
            assert type(e) is InvalidFieldValueError
            assert e.request_id is None
            assert e.error_type is ErrorType.VALIDATION.value
            assert e.error_code is ErrorCode.INVALID_FIELD_VALUE.value
            assert e.source is ErrorSource.SHIPENGINE.value
            assert (
                e.message == f"retries - Retries must be zero or greater. {retries} was provided."
            )
            with pytest.raises(InvalidFieldValueError):
                set_config_retries(retries)

    def test_invalid_timeout_provided(self):
        """DX-1443 - Invalid timeout at instantiation."""
        timeout = -5
        try:
            set_config_timeout(timeout)
        except InvalidFieldValueError as e:
            assert type(e) is InvalidFieldValueError
            assert e.request_id is None
            assert e.error_type is ErrorType.VALIDATION.value
            assert e.error_code is ErrorCode.INVALID_FIELD_VALUE.value
            assert e.source is ErrorSource.SHIPENGINE.value
            assert (
                e.message == f"timeout - Timeout must be zero or greater. {timeout} was provided."
            )
