import pytest

from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from .exceptions import CurrenciesConversionAPIException


CORRECT_PAYLOAD = {
    'currency_1': 'PLN',
    'currency_2': 'EUR',
    'amount': 100,
}

INVALID_PAYLOADS = (
    {
        'currency_1': 'PLN',
    },
    {
        'currency_1': 'PLN',
        'currency_2': 'EUR',
        'amount': 'PLN',
    },
)


class TestConvertCurrency:
    url = reverse('convert-currency')

    @patch('converter.views.perform_currency_conversion', return_value=25)
    def test_return_converted_amount_for_correct_data(
        self, perform_currency_conversion_mock, client
    ):
        response = client.post(self.url, data=CORRECT_PAYLOAD)

        assert response.status_code == status.HTTP_200_OK
        assert 'converted_amount' in response.data
        assert response.data['converted_amount'] == 25

    @pytest.mark.parametrize('payload', INVALID_PAYLOADS)
    @patch('converter.views.perform_currency_conversion')
    def test_return_error_for_invaid_data(
        self, perform_currency_conversion_mock, payload, client
    ):
        response = client.post(self.url, data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('converter.views.perform_currency_conversion')
    def test_return_error_for_currencies_conversion_api_error(
        self, perform_currency_conversion_mock, client
    ):
        perform_currency_conversion_mock.side_effect = \
            CurrenciesConversionAPIException('Some error')
        response = client.post(self.url, data=CORRECT_PAYLOAD)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.external
    def test_response_with_currencies_conversion_api(self, client):
        response = client.post(self.url, data=CORRECT_PAYLOAD)

        assert response.status_code == status.HTTP_200_OK
        assert 'converted_amount' in response.data
        # Value of converted_amount cannot be tested because it varies in case
        # of live API call
