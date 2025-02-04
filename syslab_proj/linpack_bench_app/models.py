from django.db import models
from system_test_app.models import System

import datetime

# Create your models here.
class Linpack(models.Model):
	system = models.ForeignKey(System, on_delete=models.CASCADE)
	system_bios_date = models.DateTimeField('bios_date')
	system_ipmi_version = models.CharField(max_length=50)
	tester_name = models.CharField(max_length=100)
	N = models.IntegerField(default=0)
	NB = models.IntegerField(default=0)
	PMAP = models.CharField(max_length=100)
	P = models.IntegerField(default=0)
	Q = models.IntegerField(default=0)
	PFACT = models.CharField(max_length=30)
	NBMIN = models.IntegerField(default=0)
	NDIV = models.IntegerField(default=0)
	RFACT = models.CharField(max_length=30)
	BCAST = models.CharField(max_length=30)
	DEPTH = models.IntegerField(default=0)
	SWAP = models.CharField(max_length=50)
	L1 = models.CharField(max_length=30)
	U = models.CharField(max_length=30)
	EQUIL = models.CharField(max_length=10)
	ALIGN = models.CharField(max_length=30)
	actual_GFLOPS = models.CharField(max_length=30)
	given_problem = models.CharField(max_length=150)
	expected_answer = models.CharField(max_length=30)
	answer_result = models.CharField(max_length=20)
	date_created = models.DateTimeField('date created')

	@property 
	def get_linpack_score(self):
		if self.answer_result.lower() == "passed":
			return '{0:.3f}'.format(float(self.actual_GFLOPS))
		else:
			return None

	@property
	def get_system_bios_date(self):
		return self.system_bios_date.strftime("%m/%d/%Y")


	def __str__(self):
		return self.tester_name + ": " + self.answer_result

	@property
	def get_date_created(self):
		return self.date_created.strftime("%m/%d/%y; %H:%M")