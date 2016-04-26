from rest_framework import serializers

from stockPrediction.models import *


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name',)


class OneyearstockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Oneyearstock
        fields = ('name',
                  'time',
                  'open',
                  'close',
                  'high',
                  'low',
                  'volume',)


class OnedaystockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Onedaystock
        field = (
            'name',
            'time',
            'price',
            'volume'
        )
