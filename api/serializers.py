from rest_framework import serializers

from stockPrediction.models import *


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id','name',)


class OneyearstockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Oneyearstock
        fields = ('id',
                  'name',
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
            'id',
            'name',
            'time',
            'price',
            'volume'
        )
