from rest_framework import serializers


class ConvertCurrencySerializer(serializers.Serializer):
    currency_1 = serializers.CharField(min_length=3, max_length=3)
    currency_2 = serializers.CharField(min_length=3, max_length=3)
    amount = serializers.DecimalField(max_digits=None, decimal_places=2)
    converted_amount = serializers.DecimalField(max_digits=None,
                                                decimal_places=2,
                                                read_only=True)
