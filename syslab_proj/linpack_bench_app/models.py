from django.db import models
from system_test_app.models import System

import datetime

# Create your models here.
class Linpack(models.Model):
	system = models.ForeignKey(System, on_delete=models.CASCADE)
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

	def __eq__(self, rhs):
		if self.tester_name == rhs.tester_name and \
		   self.N == rhs.N and \
		   self.NB == rhs.NB and \
		   self.PMAP == rhs.PMAP and \
		   self.P == rhs.P and \
		   self.Q == rhs.Q and \
		   self.PFACT == rhs.PFACT and \
		   self.NBMIN == rhs.NBMIN and \
		   self.NDIV == rhs.NDIV and \
		   self.RFACT == rhs.RFACT and \
		   self.BCAST == rhs.BCAST and \
		   self.DEPTH == rhs.DEPTH and \
		   self.SWAP == rhs.SWAP and \
		   self.L1 == rhs.L1 and \
		   self.U == rhs.U and \
		   self.EQUIL == rhs.EQUIL and \
		   self.ALIGN == rhs.ALIGN and \
		   self.actual_GFLOPS == rhs.actual_GFLOPS and \
		   self.given_problem == rhs.given_problem and \
		   self.expected_answer == rhs.expected_answer and \
		   self.answer_result == rhs.answer_result:

			return True

		else:
			return False

	def __hash__(self):
		return hash((self.tester_name, self.N, self.NB, self.PMAP, self.P,
		   			 self.Q, self.PFACT, self.NBMIN, self.NDIV, self.RFACT,
		   			 self.BCAST, self.DEPTH, self.SWAP, self.L1, self.U,
		   			 self.EQUIL, self.ALIGN, self.actual_GFLOPS,
		   		     self.given_problem, self.expected_answer, self.answer_result))

	def __str__(self):
		return self.tester_name + ": " + self.answer_result

	@property
	def get_date_created(self):
		return self.date_created.strftime("%m/%d/%y; %H:%M")