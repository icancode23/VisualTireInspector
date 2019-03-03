from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage
# Create your views here.

@csrf_exempt
def test(request):
	print(request)
	return HttpResponse(json.dumps({"Status":"Up"},indent=4),content_type="application/json")

@csrf_exempt
def handleFileUpload(request):
	if request.method == 'POST' and request.FILES['file']:
		uploaded_file = request.FILES['file']
		fs = FileSystemStorage()
		filename = fs.save(uploaded_file.name, uploaded_file)
		print(filename)
		uploaded_file_url = fs.url(filename)
		print (uploaded_file_url)
		return HttpResponse(json.dumps({"Status":"File Saved","FileName":uploaded_file_url},indent=4),content_type="application/json")
	return HttpResponse(json.dumps({"Status":"Invalid Request"},indent=4),content_type="application/json")