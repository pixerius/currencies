from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CurrenciesConversionAPIException
from .serializers import ConvertCurrencySerializer
from .utils import perform_currency_conversion


class ConvertCurrency(APIView):
    '''
    Endpoint for performing currency conversion based on provided amount
    and pair of currencies.
    '''
    def post(self, request, **kwargs):
        serializer = ConvertCurrencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            converted_amount = perform_currency_conversion(
                serializer.validated_data['currency_1'],
                serializer.validated_data['currency_2'],
                serializer.validated_data['amount'],
            )
        except CurrenciesConversionAPIException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response({
            **serializer.validated_data,
            'converted_amount': converted_amount,
        })
