from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from csvcoder.models import *
import utils
import csv

def index(request):
	response = render(request,'csvcoder/home.html')
	return response

def uploads(request):
	uploads = Upload.objects.values().order_by('-id')
	return utils.JsonResponse({'uploads' : list(uploads)})

def upload_file(request):
    file = request.FILES["file"]
    response = utils.save_csv(file)
    if response != "address column not found":
    	return utils.JsonResponse({'response':response})
    if response == "address column not found":
    	return utils.JsonResponse({'response':response},status= 400)

def download_csv(request,uploadid):
	# the view has to be otptimised to streaming http response for large csv files
	upload_object = get_object_or_404(Upload,pk = uploadid)
	response = HttpResponse (content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}'.format(upload_object.file_name)
	writer = csv.writer(response)
	locations = Location.objects.filter(upload_id = uploadid)
	writer.writerow(['Address','Geocode'])
	for location in locations:
		writer.writerow([location.address,location.lat_long])
	return response

