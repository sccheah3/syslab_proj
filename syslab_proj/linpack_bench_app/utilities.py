from django.utils import timezone

import zipfile
import datetime

from . import parsefile
from system_test_app.models import System, DIMM
from .models import Linpack


# parses and saves config of uploaded file
def zipfile_handler(file):
	zFiles = zipfile.ZipFile(file)
	file_list = zFiles.namelist()

	# get relative filenames
	hpl_filename = get_rel_filename(file, file_list, 'HPL.dat')
	output_filename = get_rel_filename(file, file_list, 'output')
	sysinfo_filename = get_rel_filename(file, file_list, 'sysinfo')

	print("hpl_filename: " + hpl_filename)
	print("output_filename: " + output_filename)
	print("sysinfo_filename: "  + sysinfo_filename)

	if hpl_filename == -1 or output_filename == -1 or sysinfo_filename == -1:
		return HttpResponse("Failed: File(s) is missing from zip")

	parsed_system, parsed_linpack = parse_zipfile(file, sysinfo_filename, hpl_filename, output_filename)
	save_config(parsed_system, parsed_linpack)


# gets the path to each file. Sometimes zip files have a dir with same base name as zip file
def get_rel_filename(file, file_list, base_name):
	file_without_ext = str(file)
	file_without_ext = file_without_ext.replace('.zip', '')

	if base_name in file_list:
		return base_name
	# case where it has directory with same name as zip file holding everything
	elif (file_without_ext + "/" + base_name) in file_list:	
		return file_without_ext + "/" + base_name

	return -1

# parse files and return tuple of parsed objects
def parse_zipfile(file, sysinfo_filename, hpl_filename, output_filename):
	with zipfile.ZipFile(file) as zip_file:
		sysinfo_file = zip_file.open(sysinfo_filename)
		hpl_file = zip_file.open(hpl_filename)
		output_file = zip_file.open(output_filename)

		parsed_system = parsefile.SysInfoParser(sysinfo_file)

		sysinfo_file.close()
		sysinfo_file = zip_file.open(sysinfo_filename)

		parsed_linpack = parsefile.LinpackParser(sysinfo_file, output_file)

		return (parsed_system, parsed_linpack)


# saves the system info and dimm into DB
def save_sysinfo(sysinfo):
	formatted_bios_date = datetime.datetime.strptime(sysinfo.bios_date, "%m/%d/%Y").strftime("%Y-%m-%d")
	
	system = System(motherboard_model = sysinfo.motherboard, \
		     		bios_date = formatted_bios_date, \
		   			ipmi_version = sysinfo.ipmi_version, \
		   			processor_info = sysinfo.processor, \
		   			processor_freq = sysinfo.processor_freq, \
				    processor_count = sysinfo.processor_count, \
				    total_core_count = sysinfo.processor_total_core_count, \
				    total_dimm_count = sysinfo.dimm_count, \
				    dimm_clock_speed = sysinfo.dimm_freq, \
				    dimm_memory_size = sysinfo.dimm_total_mem_size, \
				    processor_family = sysinfo.processor_family, \
				    hpl_block_size = sysinfo.HPL_block_size, \
				    hpl_problem_size = sysinfo.HPL_problem_size, \
				    linpack_theoretical_score = sysinfo.linpack_theoretical_GFLOPS, \
					date_created = timezone.now(), \
					date_modified = timezone.now())

	system.save()

	if len(sysinfo.dimm_manu_list) == len(sysinfo.dimm_PN_list):
		for i in range(len(sysinfo.dimm_manu_list)):
			system.dimm_set.create(manufacturer = sysinfo.dimm_manu_list[i], \
								   part_number = sysinfo.dimm_PN_list[i], \
								   date_created = timezone.now())

	system.save()

	return system

# saves linpack info associated with system to DB
def save_linpackinfo(system, linpack_info):

	system.linpack_set.create(tester_name = linpack_info.tester_name, \
					  		  N = linpack_info.N, \
					  		  NB = linpack_info.NB, \
					  		  PMAP = linpack_info.PMAP, \
					  		  P = linpack_info.P, \
							  Q = linpack_info.Q, \
							  PFACT = linpack_info.PFACT, \
							  NBMIN = linpack_info.NBMIN, \
							  NDIV = linpack_info.NDIV, \
							  RFACT = linpack_info.RFACT, \
							  BCAST = linpack_info.BCAST, \
							  DEPTH = linpack_info.DEPTH, \
							  SWAP = linpack_info.SWAP, \
							  L1 = linpack_info.L1, \
							  U = linpack_info.U, \
							  EQUIL = linpack_info.EQUIL, \
							  ALIGN = linpack_info.ALIGN, \
							  actual_GFLOPS = linpack_info.actual_GFLOPS, \
							  given_problem = linpack_info.given_problem, \
							  expected_answer = linpack_info.expected_answer, \
							  answer_result = linpack_info.answer_result,\
							  date_created = timezone.now())

	system.save()


# check to see if there's an existing System entry with this config
# @return system or False
def get_existing_config(parsed_system):
	systems = System.objects.filter(
				motherboard_model = parsed_system.motherboard, \
				bios_date = datetime.datetime.strptime(parsed_system.bios_date, "%m/%d/%Y").strftime("%Y-%m-%d"), \
				processor_info = parsed_system.processor, \
				processor_freq = parsed_system.processor_freq, \
				processor_count = parsed_system.processor_count, \
				total_core_count = parsed_system.processor_total_core_count, \
				total_dimm_count = parsed_system.dimm_count, \
				dimm_clock_speed = parsed_system.dimm_freq, \
				dimm_memory_size = parsed_system.dimm_total_mem_size, \
				processor_family = parsed_system.processor_family
			 )

	# check if any matches
	if not systems:
		return None
	
	# will return system if dimm config exists, else return none
	return get_dimm_system_match(systems, parsed_system)


# searches through systems for matching dimm config with parsed system
# @return system match
def get_dimm_system_match(systems, parsed_system):
	if systems is None: 
		return

	for system in systems:
		dimms = system.dimm_set.all()

		dimm_manu_list = parsed_system.dimm_manu_list[:]
		dimm_PN_list = parsed_system.dimm_PN_list[:]

		for i in range(0, len(dimms)):
			if (i == 0) and (len(dimms) != len(dimm_manu_list)):
				break

			try:
				dimm_manu_list.remove(dimms[i].manufacturer)
				dimm_PN_list.remove(dimms[i].part_number)
			except ValueError:
				pass

		if len(dimm_manu_list) == 0 and len(dimm_PN_list) == 0:
			return system

	return None



# saves the parsed system whether it is new entry or appended linpack score
def save_config(parsed_system, parsed_linpack):
	system = get_existing_config(parsed_system)

	if system:
		save_linpackinfo(system, parsed_linpack)
	else:
		system = save_sysinfo(parsed_system)
		save_linpackinfo(system, parsed_linpack)
