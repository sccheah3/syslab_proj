from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from . import parsefile
import zipfile
import datetime

from system_test_app.models import System, DIMM
from .models import Linpack


# files < 2.5 MB stored in mem. Files > are stored in a tmp folder
# curl --form title=TestTitle --form file=@test.txt http://127.0.0.1:8000/linpack_bench/upload_zipfile/
@csrf_exempt	# can be dangerous with bad request. ASSUMPTION: no one will do anything dumb or malicious
def upload_zipfile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			file = request.FILES['file']

			if zipfile.is_zipfile(file):
				print("This is a valid zipfile")

				zFile = zipfile.ZipFile(file)
				file_list = zFile.namelist()

				# if directory has same name inside zip file without .zip ext
				file_without_ext = str(file)
				file_without_ext = file_without_ext.replace('.zip', '')

				hpl_filename = get_filename(file_list, file_without_ext, 'HPL.dat')
				output_filename = get_filename(file_list, file_without_ext, 'output')
				sysinfo_filename = get_filename(file_list, file_without_ext, 'sysinfo')

				print("hpl_filename: " + hpl_filename)
				print("output_filename: " + output_filename)
				print("sysinfo_filename: " + sysinfo_filename)

				if hpl_filename == -1 or output_filename == -1 or sysinfo_filename == -1:
					return HttpResponse("Failed: File(s) is missing from zip")

				# create a separate module to parse these files and input into database

				with zipfile.ZipFile(file) as zip_file:
					sysinfo_file = zip_file.open(sysinfo_filename)
					hpl_file = zip_file.open(hpl_filename)
					output_file = zip_file.open(output_filename)

					system = save_sysinfo(parsefile.SysInfoParser(sysinfo_file))

					# TODO: unable to seek(0). find fix for this
					sysinfo_file.close()
					sysinfo_file = zip_file.open(sysinfo_filename)

					save_linpackinfo(system, parsefile.LinpackParser(sysinfo_file, output_file))



			else:
				return HttpResponse("Failed: Not a valid zipfile.")


			# print(request.POST['title'])

			return HttpResponse("Success\n")
	else:
		form = UploadFileForm()

	return render(request, 'linpack_bench_app/upload.html', {'form': form})


def linpack_db(request):
	return render(request, 'linpack_bench_app/linpack_db.html', {'systems': System.objects.all()})

def index(request):
	return HttpResponse("Hello world!")


def detail(request, system_id):
	system = System.objects.get(id=system_id)

	return render(request, 'linpack_bench_app/linpack_detail.html', {
		'system': system, 
		'dimms': system.dimm_set.all(),
		'linpacks': system.linpack_set.all(),
	})



# utility functions
def file_exists(filename_list, filename):
	if (filename in filename_list):
		return True

	return False

def get_filename(file_list, file_without_ext, base_name):
	if base_name in file_list:
		return base_name
	elif (file_without_ext + "/" + base_name):
		return file_without_ext + "/" + base_name

	return -1

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
					date_added = timezone.now())

	system.save()

	if len(sysinfo.dimm_manu_list) == len(sysinfo.dimm_PN_list):
		for i in range(len(sysinfo.dimm_manu_list)):
			system.dimm_set.create(manufacturer = sysinfo.dimm_manu_list[i], \
								   part_number = sysinfo.dimm_PN_list[i], \
								   date_added = timezone.now())

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
							  date_added = timezone.now())

	system.save()
