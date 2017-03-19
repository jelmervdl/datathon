import csv
import json

user_locations = dict()

with open('data/social/twitter_cikm_2010/training_set_users.txt', 'r') as fh:
	for line in fh:
		user, city_name = line.split('\t', 2)
		user_locations[user] = city_name.strip()

locations = dict()

with open('/Users/jelmer/Downloads/locations.txt.html', 'r') as fh:
	reader = csv.DictReader(fh, delimiter='\t')
	for row in reader:
		locations[row['Address']] = {
            'lat': float(row['Latitude']),
            'long': float(row['Longitude'])
        }

for user, location in user_locations.items():
	if location in locations:
		user_locations[user] = locations[location]

with open('user-locations.json', 'w') as fh:
	json.dump(user_locations, fh, indent=2)

