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


	@property
	def dimm_data(self):
		dimms = self.dimm_set.all()

		dimm_dict = {}
		output = ""

		for dimm in dimms:
			if dimm.part_number not in dimm_dict.keys():
				dimm_dict[dimm.part_number] = 1
			else:
				dimm_dict[dimm.part_number] += 1

		for i in dimm_dict:
			output += str(dimm_dict[i]) + ': ' + i + ', '

		return output

	@property
	def linpack_actual_data(self):
		linpacks = self.linpack_set.all()

		output = ""

		for linpack in linpacks:
			output += linpack.actual_GFLOPS + ", "

		return output
	
	def __eq__(self, rhs):
		if self.motherboard_model == rhs.motherboard_model and \
		   self.bios_date == rhs.bios_date and \
		   self.ipmi_version == rhs.ipmi_version and \
		   self.processor_info == rhs.processor_info and \
		   self.processor_freq == rhs.processor_freq and \
		   self.processor_count == rhs.processor_count and \
		   self.total_core_count == rhs.total_core_count and \
		   self.total_dimm_count == rhs.total_dimm_count and \
		   self.dimm_clock_speed == rhs.dimm_clock_speed and \
		   self.dimm_memory_size == rhs.dimm_memory_size and \
		   self.processor_family == rhs.processor_family and \
		   self.hpl_block_size == rhs.hpl_block_size and \
		   self.hpl_problem_size == rhs.hpl_problem_size and \
		   self.linpack_theoretical_score == rhs.linpack_theoretical_score:

		   	return True

		else:
			return False


	def __hash__(self):
		return hash((self.motherboard_model, self.bios_date, self.ipmi_version,
					 self.processor_info, self.processor_freq, self.processor_count,
					 self.total_core_count, self.total_dimm_count, self.dimm_clock_speed,
					 self.dimm_memory_size, self.processor_family, self.hpl_block_size,
					 self.hpl_problem_size, self.linpack_theoretical_score))


	def __str__(self):
		return self.motherboard_model



class DIMM(models.Model):
	system = models.ForeignKey(System, on_delete=models.CASCADE)
	manufacturer = models.CharField(max_length=400)
	part_number = models.CharField(max_length=350)
	date_added = models.DateTimeField('date added')


	def __eq__(self, rhs):
		if self.manufacturer == rhs.manufacturer and \
		   self.part_number == rhs.part_number:
		   	return True

		else:
			return False

	def __hash__(self):
		return hash((self.manufacturer, self.part_number))


	def __str__(self):
		return self.manufacturer + " " + self.part_number
