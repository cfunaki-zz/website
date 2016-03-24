from django.db import models

class ZipCode(models.Model):
	zipcode = models.CharField(max_length=5)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=2)
	latitude = models.FloatField()
	longitude = models.FloatField()
	timezone = models.IntegerField()
	dst = models.IntegerField()

class Crime(models.Model):
	crime_id = models.IntegerField(primary_key=True)
	datetime = models.DateTimeField()
	zipcode = models.ForeignKey(ZipCode)
	latitude = models.FloatField()
	longitude = models.FloatField()
	victims = models.IntegerField()
	gang = models.BooleanField()
	violent = models.BooleanField()