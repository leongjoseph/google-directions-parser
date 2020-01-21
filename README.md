# Google Directions Parser

Simple Python parser for Google Directions API data.

## Depedencies 

Ensure that the following dependencies are installed on your computer:

- numpy
- pandas 
- requests

## Typical Usage

1. Download the python file
2. Create new python file in the same directory as 'google-directions-parser.py'
3. Usage of the parser is as follows:

```python
import google-directions-parser as gds

key = 'abc'                 # Google Directions API key
origlat = '-37.89702141'    # origin latitude coodinate 
origlon = '144.9921144'     # origin longitudinal coordinate
destlat = '-37.80506789'    # destination latitude coordinate
destlon = '144.9814108'     # destination longitudinal coordinate
startime = '1110'           # start time of trip (minutes past midnight)
travdate = '1/8/14'         # date as per date stated in VISTA dataset

all_mode_info = gds.gmaps(key, origlat, origlon, destlat, destlon, startime, travdate).getAll()

```

This will return a Dict object containing (for the above example):

```python

{'cycling_cycle_time': 2984,
 'cycling_distance': 13735,
 'driving_distance': 12274,
 'driving_duration_wTraffic': 2199,
 'driving_duration_woTraffic': 1611,
 'end_address': '20 Little Gore St, Fitzroy VIC 3065, Australia',
 'start_address': '6 Drake St, Brighton VIC 3186, Australia',
 'transit_distance': 14564,
 'transit_transfers': 2,
 'transit_transit_time': 3300,
 'transit_walk_time': 1045,
 'walking_distance': 11541,
 'walking_walk_time': 8968}
 
 ```
 ### Mode Specific Usage
 
 Alternatively, if data for a single mode is required - use the following:

 Note that it can be specified whether address (bool) is required as an output.
 
 #### Car

 Input:
 
 ```python
 car_mode_info = gds.gmaps(key, origlat, origlon, destlat, destlon, startime, travdate).driveFetch(address=True) 
 ```
 Output:

 ```python
 {'driving_distance': 12274,
  'driving_duration_wTraffic': 2212,
  'driving_duration_woTraffic': 1611,
  'end_address': '20 Little Gore St, Fitzroy VIC 3065, Australia',
  'start_address': '6 Drake St, Brighton VIC 3186, Australia'}
  ```
 #### Bicycle

 Input:
 
 ```python
 bicycle_mode_info = gds.gmaps(key, origlat, origlon, destlat, destlon, startime, travdate).cycleFetch(address=False) 
```
Output:

```python
{'cycling_cycle_time': 2984, 'cycling_distance': 13735}
```
 
#### Transit 

 Input:
 
 ```python
 transit_mode_info = gds.gmaps(key, origlat, origlon, destlat, destlon, startime, travdate).transitFetch(address=False) 
```
Output:

```python
{'transit_distance': 14564,
 'transit_transfers': 2,
 'transit_transit_time': 3300,
 'transit_walk_time': 1045}
```

#### Walking

Input:

```python
walk_mode_info = gds.gmaps(key, origlat, origlon, destlat, destlon, startime, travdate).cycleFetch(address=True)
```

Output:

```python
{'end_address': '20 Little Gore St, Fitzroy VIC 3065, Australia',
 'start_address': '6 Drake St, Brighton VIC 3186, Australia',
 'walking_distance': 11541,
 'walking_walk_time': 8968}
```



 
 
 


 




