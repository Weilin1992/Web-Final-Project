from django.db import models


class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'stockPrediction_company'


class  Onedaystock(models.Model):
    time = models.DateTimeField(primary_key=True)
    price = models.FloatField()
    volume = models.IntegerField()
    name = models.ForeignKey(Company, models.DO_NOTHING, db_column='name',primary_key=True)

    class Meta:
        managed = False
        db_table = 'stockPrediction_onedaystock'


class Oneyearstock(models.Model):
    name = models.ForeignKey(Company, models.DO_NOTHING, db_column='name',primary_key=True)
    time = models.DateField(primary_key=True)
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stockPrediction_oneyearstock'
        unique_together = (('name', 'time'),)
