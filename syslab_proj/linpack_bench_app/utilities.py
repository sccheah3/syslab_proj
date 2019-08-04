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

	parse_zipfile(file, sysinfo_filename, hpl_filename, output_filename)


def get_rel_filename(file, file_list, base_name):
	file_without_ext = str(file)
	file_without_ext = file_without_ext.replace('.zip', '')

	if base_name in file_list:
		return base_name
	# case where it has directory with same name as zip file holding everything
	elif (file_without_ext + "/" + base_name) in file_list:	
		return file_without_ext + "/" + base_name

	return -1


def parse_zipfile(file, sysinfo_filename, hpl_filename, output_filename):
	with zipfile.ZipFile(file) as zip_file:
		sysinfo_file = zip_file.open(sysinfo_filename)
		hpl_file = zip_file.open(hpl_filename)
		output_file = zip_file.open(output_filename)

		system = save_sysinfo(parsefile.SysInfoParser(sysinfo_file))

		sysinfo_file.close()
		sysinfo_file = zip_file.open(sysinfo_filename)

		save_linpackinfo(system, parsefile.LinpackParser(sysinfo_file, output_file))


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


def config_exists(parsed_system, parsed_linpack):
	pass # use System.objects.filter(...)

	# check to see if there's an existing System entry with this config
	systems = System.objects.filter(
				motherboard_model = parsed_system.motherboard, \
				bios_date = datetime.datetime.strptime(parsed_system.bios_date, "%m/%d/%Y").strftime("%Y-%m-%d"), \
				ipmi_version = parsed_system.ipmi_version, \
				processor_info = parsed_system.processor, \
				processor_freq = parsed_system.processor_freq, \
				processor_count = parsed_system.processor_count, \
				total_core_count = parsed_system.processor_total_core_count, \
				total_dimm_count = parsed_system.dimm_count, \
				dimm_clock_speed = parsed_system.dimm_freq, \
				dimm_memory_size = parsed_system.dimm_total_mem_size, \
				processor_family = parsed_system.processor_family, \
				hpl_block_size = parsed_system.HPL_block_size, \
				hpl_problem_size = parsed_system.HPL_problem_size, \
				linpack_theoretical_score = parsed_system.linpack_theoretical_GFLOPS
			 )

	# check if 
	if not systems:
		return False
	else:
		# check dimm config
		for system in systems:
			dimm_map = {}
			dimm_match = True

			# get counts for each PN
			for pn in parsed_system.dimm_PN_list:
				if pn in dimm_map:
					dimm_map[pn] += 1
				else:
					dimm_map[pn] = 1

			for dimm in system.dimm_set.all():
				if dimm.part_number not in dimm_map:
					break
				else:
					dimm_map[dimm.part_number] -= 1

			for pn in dimm_map:
				if dimm_map[pn] != 0:
					dimm_match = False
					break

			if not dimm_match:
				continue
			else:
				linpack_match = False
				# check for linpack config
				for linpack in system.linpack_set.all():
					if (linpack.tester_name == parsed_linpack.tester_name, \
					  	linpack.N == parsed_linpack.N, \
					  	linpack.NB == parsed_linpack.NB, \
					  	linpack.PMAP == parsed_linpack.PMAP, \
					  	linpack.P == parsed_linpack.P, \
						linpack.Q == parsed_linpack.Q, \
						linpack.PFACT == parsed_linpack.PFACT, \
						linpack.NBMIN == parsed_linpack.NBMIN, \
						linpack.NDIV == parsed_linpack.NDIV, \
						linpack.RFACT == parsed_linpack.RFACT, \
						linpack.BCAST == parsed_linpack.BCAST, \
						linpack.DEPTH == parsed_linpack.DEPTH, \
						linpack.SWAP == parsed_linpack.SWAP, \
						linpack.L1 == parsed_linpack.L1, \
						linpack.U == parsed_linpack.U, \
						linpack.EQUIL == parsed_linpack.EQUIL, \
						linpack.ALIGN == parsed_linpack.ALIGN, \
						linpack.actual_GFLOPS == parsed_linpack.actual_GFLOPS, \
						linpack.given_problem == parsed_linpack.given_problem, \
						linpack.expected_answer == parsed_linpack.expected_answer, \
						linpack.answer_result == parsed_linpack.answer_result):	

						linpack_match = True
						break

				if not linpack_match:
					save_linpackinfo(system, parsed_linpack)

				return True

	return False

def save_config(parsed_system, parsed_linpack):
	system = save_sysinfo(parsed_system)
	save_linpackinfo(system, parsed_linpack)
