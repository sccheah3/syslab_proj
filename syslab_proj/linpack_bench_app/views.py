from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from . import utilities
import zipfile

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
				utilities.zipfile_handler(file)

				return HttpResponse("Success\n")
			else:
				return HttpResponse("Failed: Not a valid zipfile.")
	else:
		form = UploadFileForm()

	return render(request, 'linpack_bench_app/upload.html', {'form': form})


def performance_comparison(request):
	res = []

	for key in request.POST:
		if key.startswith('system'):
			res.append(key)

	#return HttpResponse(str(res))
	return HttpResponse(request.POST.get(res[0]))

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
