from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from bulk_update.helper import bulk_update
from csvcoder.models import *
from geocoder.settings import *
from openpyxl import load_workbook
import requests
import json
import tasks
import csv


class JsonResponse(HttpResponse):
    def __init__(self, content={}, status=None, content_type='application/json'):
        super(JsonResponse,self).__init__(json.dumps(content,cls=DjangoJSONEncoder),
                                           status=status, content_type=content_type)
def save_csv(file):
	csv_file = file
	wb = load_workbook(csv_file)
	ws = wb.worksheets[0]
	rows = ws.rows
	row1 = next(rows)
	row1 = [x.value.lower() for x in row1]
	if "address" not in row1:
		return "address column not found"
	else:
		upload_object = Upload.objects.create(file_name = file.name,size = csv_file.size)
		address_index = row1.index('address')
		location_objects = [Location(address = row[address_index].value,upload_id= upload_object.id) for row in rows]
		Location.objects.bulk_create(location_objects)
		tasks.query_geocodes.delay(upload_object.id)
		return upload_object.id


def geocode_rows(upload = None):
	retry = False
	addresses = Location.objects.filter(is_geocoded = 1)
	if upload is not None:
		addresses = addresses.filter(upload_id = upload)
	for address in addresses:
		gecode_url = GEOCODE_URL.format(address.address,API_KEY)
		response = requests.get(gecode_url).json()
		if response['status'] == 'OK':
			results = response['results']
			if len(results)  >  0:
				result = results[0]
				lat = result['geometry']['location']['lat']
				lng = result['geometry']['location']['lng']
			else:
				lat=lng = ''
			address.lat_long = str(lat)+','+str(lng)
			address.is_geocoded = 2
		elif results['status'] == 'OVER_QUERY_LIMIT':
			retry = True
			break
	bulk_update(addresses,update_fields=['is_geocoded','lat_long'])
	if retry == False:
		upload_obj = Upload.objects.get(pk = upload)
		upload_obj.geocoding_status = 2
		upload_obj.save()
	return retry