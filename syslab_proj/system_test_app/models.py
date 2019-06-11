from django.db import models
from django.utils import timezone
import datetime

class System(models.Model):
	motherboard_model = models.CharField(max_length=200)
	bios_date = models.DateTimeField('bios_date')
	ipmi_version = models.CharField(max_length=50)
	processor_info = models.CharField(max_length=300)
	processor_freq = models.CharField(max_length=200)
	processor_count = models.IntegerField(default=0)
	total_core_count = models.IntegerField(default=0)
	total_dimm_count = models.IntegerField(default=0)
	dimm_clock_speed = models.CharField(max_length=200)
	dimm_memory_size = models.CharField(max_length=200)
	processor_family = models.CharField(max_length=300)
	hpl_block_size = models.IntegerField(default=0)
	hpl_problem_size = models.IntegerField(default=0)
	linpack_theoretical_score = models.CharField(max_length=300)
	date_added = models.DateTimeField('date added')

	def __str__(self):
		return self.motherboard_model



class DIMM(models.Model):
	system = models.ForeignKey(System, on_delete=models.CASCADE)
	manufacturer = models.CharField(max_length=400)
	part_number = models.CharField(max_length=350)
	date_added = models.DateTimeField('date added')

	def __str__(self):
		return self.manufacturer + " " + self.part_number
