from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.files.storage import FileSystemStorage
from utils import predict_defect
# Create your views here.

@csrf_exempt
def test(request):
	print(request)
	return HttpResponse(json.dumps({"Status":"Up"},indent=4),content_type="application/json")


@csrf_exempt
def handleFileUpload(request):
	info = {"Crown Deformation" : "Refers to change in shape of the tire at the crown area and results in wobbling of the vehicle.",
    "Extruding Stamp Ink" : "It is a defect which causes the tire to burst due to more ink contaminated. The tire is OK if the ink spot diameter is less than 4mm and is kept away from the distance of 1/4 or more of the tire circumference else it is NG.",
    "Scorched Rubber Tire" : "Respective areas side tread may separate during high speed of vehicles.",
    "Bladder Crease" : "Tire tube becomes damaged during the curing process and leaves creases on the inner side of the tire.",
    "Liner Air" : "It refers to the bubble or blister in the tire due to adhesion loss of inner liner material to the casing."}
	if request.method == 'POST' and request.FILES['file']:
		uploaded_file = request.FILES['file']
		base_url = "/home/vasu/all_projects/SIH/VisualTireInspectorBackend"
		fs = FileSystemStorage()
		filename = fs.save("test.jpeg", uploaded_file)
		print(filename)
		uploaded_file_url = fs.url(filename)
		print (uploaded_file_url)
		score = predict_defect(base_url + uploaded_file_url)
		return HttpResponse(json.dumps({"result":score,"info":[info["Liner Air"],info["Bladder Crease"], info["Scorched Rubber Tire"], info["Crown Deformation"],info["Extruding Stamp Ink"]]},indent=4),content_type="application/json")
	return HttpResponse(json.dumps({"Status":"Invalid Request"},indent=4),content_type="application/json")