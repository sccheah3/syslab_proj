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
	date_created = models.DateTimeField('date created')
	date_modified = models.DateTimeField('date modified')


	@property 
	def get_motherboard_model(self):
		return str(self.motherboard_model)

	# remove 'family' when displaying on table. can refactor with regex
	@property 
	def get_processor_family(self):
		output = self.processor_family.replace('Family', '');
		return output.replace('family', '');

	@ property
	def get_processor_info(self):
		return str(self.processor_info)
		 

	@property
	def get_dimm_memory_size(self):
		return str("{:.2f}".format(float(self.dimm_memory_size.replace('GB', ''))) + ' GB')

	@property
	def get_dimm_freq(self):
		return str(self.dimm_clock_speed)
	

	@property
	def get_bios_date(self):
		return self.bios_date.strftime("%m/%d/%Y")
	
	@property
	def get_date_created(self):
		return self.date_created.strftime("%m/%d/%y; %H:%M")

	@property
	def get_date_modified(self):
		return self.date_modified.strftime("%m/%d/%y; %H:%M")

	@property
	def get_detailed_dimm_pn_data(self):
		dimms = self.dimm_set.all()

		dimm_dict = {}
		output = ""

		for dimm in dimms:
			if dimm.part_number not in dimm_dict.keys():
				dimm_dict[dimm.part_number] = 1
			else:
				dimm_dict[dimm.part_number] += 1

		for i in dimm_dict.keys():
			output += str(dimm_dict[i]) + ': ' + i + '; '

		return output

	@property
	def get_dimm_pn_data(self):
		dimms = self.dimm_set.all()

		dimm_set = set()
		output = ""

		for dimm in dimms:
			dimm_set.add(dimm.part_number)

		if len(dimm_set) == 1:
			return "".join(str(pn) for pn in dimm_set)
		else:
			return "; ".join(str(pn) for pn in dimm_set)

	@property
	def get_dimm_manu_data(self):
		dimms = self.dimm_set.all()

		dimm_set = set()
		output = ""

		for dimm in dimms:
			dimm_set.add(dimm.manufacturer)

		if len(dimm_set) == 1:
			return "".join(str(man) for man in dimm_set)
		else:
			return "; ".join(str(man) for man in dimm_set)


	@property 
	def get_linpack_highest_actual(self):
		linpacks = self.linpack_set.all()
		linpack_actuals = [float(linpack.actual_GFLOPS) for linpack in linpacks if (linpack.answer_result.lower() == "passed")]

		if len(linpack_actuals) != 0:
			return '{0:.3f}'.format(max(linpack_actuals))
		else:
			return None

	@property 
	def get_linpack_lowest_actual(self):
		linpacks = self.linpack_set.all()
		linpack_actuals = [float(linpack.actual_GFLOPS) for linpack in linpacks if (linpack.answer_result.lower() == "passed")]

		if len(linpack_actuals) != 0:
			return '{0:.3f}'.format(min(linpack_actuals))
		else:
			return None

	@property
	def get_linpack_avg_actual(self):
		linpacks = self.linpack_set.all()

		linpack_actuals = [float(linpack.actual_GFLOPS) for linpack in linpacks if (linpack.answer_result.lower() == "passed")]

		if len(linpack_actuals) != 0:
			linpack_avg = sum(linpack_actuals) / len(linpack_actuals)

			return '{0:.3f}'.format(linpack_avg)
		else:
			return None

	@property
	def get_linpack_avg_actual_data(self):
		linpacks = self.linpack_set.all()

		linpack_actuals = [float(linpack.actual_GFLOPS) for linpack in linpacks if (linpack.answer_result.lower() == "passed")]

		if len(linpack_actuals) != 0:
			linpack_avg = sum(linpack_actuals) / len(linpack_actuals)

			return str("{:.2f}".format(float(linpack_avg))) + " GFLOPS"
		else:
			return "N/A"


	def __str__(self):
		return self.motherboard_model



class DIMM(models.Model):
	system = models.ForeignKey(System, on_delete=models.CASCADE)
	manufacturer = models.CharField(max_length=400)
	part_number = models.CharField(max_length=350)
	date_created = models.DateTimeField('date created')

	def __str__(self):
		return self.manufacturer + " " + self.part_number
