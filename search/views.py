from django.shortcuts import render
import xml.etree.ElementTree as ET
import math
import requests
import json

def index(request):

	data = {
		'api_key': 't8s9ekw59e3pwec5856pt9w8',
		'town':'pangbourne',
		'county':'berkshire',
		'radius':20,
		'listing_status':'rent',
		'maximum_price':250,
		'maximum_beds':2,
		'order_by':'age',
		}
	r = requests.get('http://api.zoopla.co.uk/api/v1/property_listings', params=data)

	if r.status_code == 200:
		context = {'listings':generate_listings(r.text.encode('utf-8').strip())}
	else:
		url = r.url
		r.raise_for_status()

	return render(request, 'search_index.html', context)


def generate_listings(xml):
	root = ET.fromstring(xml)

	rdg = [51.458546, -0.972097]
	
	output = []

	for listing in root.findall("listing"):
		coords = [float(listing.find('latitude').text), float(listing.find('longitude').text)]
		output.append({'address': listing.find('displayable_address').text, 'distance': distance(rdg,coords)})

	return output

def distance(origin, destination):
	lat1, lon1 = origin
	lat2, lon2 = destination
	#radius = 6371 # km
	radius = 3958.75587 #miles

	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c

	return d