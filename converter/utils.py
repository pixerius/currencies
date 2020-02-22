import requests

from decimal import Decimal

from django.conf import settings
from requests.exceptions import RequestException

from .exceptions import CurrenciesConversionAPIException


def perform_currency_conversion(
    currency_1: str, currency_2: str, amount: Decimal
) -> Decimal:
    '''
    Uses external API to perform currency conversion with provided arguments:
    :param currency_1: source currency
    :param currency_2: conversion result currency
    :param amount: amount of money in source currency
    :return: converted amount
    :raises CurrenciesConversionAPIException: in case of external API error
    '''
    try:
        response = requests.get(
            settings.CURRENCIES_CONVERSION_API_URL,
            params={
                'base': currency_1,
                'symbols': currency_2,
            })
        response.raise_for_status()
    except RequestException as e:
        raise CurrenciesConversionAPIException(str(e))

    try:
        json_data = response.json()  # possibly raises ValueError
        rate = json_data['rates'][currency_2]
    except (ValueError, KeyError, TypeError):
        raise CurrenciesConversionAPIException(
            'Unexpceted currencies conversion API response'
        )

    return amount * Decimal(rate)
