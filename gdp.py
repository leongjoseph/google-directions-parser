import requests
import time
import pandas as pd
import datetime

class Get:
    def __init__(self, key, orig_lat, orig_lon, dest_lat, dest_lon, time, date, saveJson=False):
        self.key = str(key)
        self.origlat = str(orig_lat)
        self.origlon = str(orig_lon)
        self.destlat = str(dest_lat)
        self.destlon = str(dest_lon)
        self.timeTimestamp = str(self.dateToTimestamp(date) + int(time) * 60)
        self.saveJson = saveJson
        
    def response(self, mode): 
        url = 'https://maps.googleapis.com/maps/api/directions/json?'

        parameters = \
        {
            'key': self.key,
            'origin': self.origlat + ',' + self.origlon,
            'destination': self.destlat + ',' + self.destlon,
            'units': 'metric',
            'departure_time': self.timeTimestamp,
            'mode': mode
        }
        
        if mode == 'transit':
            parameters.update({'transit_mode': 'train|tram|bus',
                               'transit_routing_preference': 'fewer_transfers'})

        success = False
        while not success:
            try:
                request = requests.get(url, params=parameters)
                data = request.json()
                success = True
                return data
            
            except Exception as e:
                print("Error: %s" % (str(e)))
                print("Retrying in 5 seconds...")
                time.sleep(5)
    
    def transitFetch(self, address=True):
        data = self.response('transit')

        if address:
            values = self.constData(data)
        else:
            values = {}

        if 'available_travel_modes' in data:
            data = self.response('walking')
        
        mainData = data['routes'][0]['legs'][0]['steps']

        transit_distance = data['routes'][0]['legs'][0]['distance']['value']
        transit_walk_time = 0
        transit_transit_time = 0
        transit_transfers = 0
        
        for i in range(len(mainData[:])):
            if mainData[i]['travel_mode'] == "WALKING":
                transit_walk_time += mainData[i]['duration']['value']
            elif mainData[i]['travel_mode'] == "TRANSIT":
                transit_transit_time += mainData[i]['duration']['value']
                transit_transfers += 1
        
        if transit_transfers < 0:
            transit_transfers = 0
        
        values.update({'transit_walk_time': transit_walk_time,
                        'transit_transit_time': transit_transit_time,
                        'transit_transfers': transit_transfers,
                        'transit_distance': transit_distance})
        
        return values
                
    def walkFetch(self, address=True):
        data = self.response('walking')
        if address == True:
            values = self.constData(data)
        else:
            values = {}

        mainData = data['routes'][0]['legs'][0]['steps']
        walking_distance = data['routes'][0]['legs'][0]['distance']['value']
        walking_walkTime = 0
        
        for i in range(len(mainData[:])):
            if mainData[i]['travel_mode'] == 'WALKING':
                walking_walkTime += mainData[i]['duration']['value']

        values.update({'walking_walk_time': walking_walkTime,
                        'walking_distance': walking_distance})

        return values

    def cycleFetch(self, address=True):
        data = self.response('bicycling')
        if address == True:
            values = self.constData(data)
        else:
            values = {}

        mainData = data['routes'][0]['legs'][0]['steps']
        cycling_distance = data['routes'][0]['legs'][0]['distance']['value']
        cycling_travelTime = 0

        for i in range(len(mainData[:])):
            if mainData[i]['travel_mode'] == 'BICYCLING':
                cycling_travelTime += mainData[i]['duration']['value']

        values.update({'cycling_cycle_time': cycling_travelTime,
                       'cycling_distance': cycling_distance})
        
        return values

    def driveFetch(self, address=True):
        data = self.response('driving')
        if address:
            values = self.constData(data)
        else:
            values = {}
        
        driving_distance = data['routes'][0]['legs'][0]['distance']['value']
        driving_duration_wTraffic = data['routes'][0]['legs'][0]['duration_in_traffic']['value']
        driving_duration_woTraffic = data['routes'][0]['legs'][0]['duration']['value']
 
        values.update({'driving_duration_woTraffic': driving_duration_woTraffic,
                       'driving_duration_wTraffic': driving_duration_wTraffic,
                       'driving_distance': driving_distance})
        
        return values
       
    def getAll(self):
        values = {}
        values.update(self.driveFetch(address=True))
        values.update(self.transitFetch(address=False))
        values.update(self.walkFetch(address=False))
        values.update(self.cycleFetch(address=False))
        
        return values
       
    def constData(self, data):
        values = \
        {
            'start_address': data['routes'][0]['legs'][0]['start_address'],
            'end_address': data['routes'][0]['legs'][0]['end_address'],
        }

        return values

    def dateToTimestamp(self, dateString):
        currentYear = datetime.datetime.now().year
        dateArray = dateString.split('/')
        dateArray = [int(i) for i in dateArray]
        ts = int(datetime.datetime(currentYear + 1, dateArray[1], dateArray[0]).timestamp()) + 10 * 3600

        return ts

def csv_parser(csv_file):
    try:
        df = pd.read_csv(csv_file, header=0)
        df = df.dropna()

    except Exception as e:
        print("Import Error: " + str(e))

    return df

