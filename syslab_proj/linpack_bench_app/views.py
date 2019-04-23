from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UploadFileForm

from django.views.decorators.csrf import csrf_exempt


# files < 2.5 MB stored in mem. Files > are stored in a tmp folder
# curl --form title=TestTitle --form file=@test.txt http://127.0.0.1:8000/linpack_bench/upload_file/
@csrf_exempt	# can be dangerous with bad request. ASSUMPTION: no one will do anything dumb or malicious
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			file = request.FILES['file']

			print(request.POST['title'])
			for line in file:
				print(line.decode())	# does not show special characters. i.e. \n

			return HttpResponse("Success")
	else:
		form = UploadFileForm()

	return render(request, 'upload.html', {'form': form})


def index(request):
	return HttpResponse("Hello world!")