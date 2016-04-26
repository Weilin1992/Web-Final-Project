from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    # class Meta:
    #     managed = False
    #     db_table = 'stockPrediction_company'


class Onedaystock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    time = models.DateTimeField()
    price = models.FloatField()
    volume = models.FloatField()

    # class Meta:
    #     managed = False
    #     db_table = 'stockPrediction_onedaystock'


class Oneyearstock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    time = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    # class Meta:
    #     managed = False
    #     db_table = 'stockPrediction_oneyearstock'
