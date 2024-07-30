import time
import datetime
import requests
import json
import os

# Flight Status

def api_url_generator(host, appID, apiKey):
    print("How would you like to search for your flight?")
    method = input("By Route or Flight_ID? {route, id}: ")
    url = host
    os.system('clear')

    if method.lower() in ["route", "r"]:
        url += "route/status/"

        # Adding the Departure and Arrival Airports
        print("Please Enter the 3 Character Code for the Airports (Ex. LHR - London Heathrow, DOH - Doha Hamad Int'l)")
        from_air = input("From: ").upper()
        to_air = input("To: ").upper()
        url += f"{from_air}/{to_air}/dep/"
        
        os.system('clear')

        # Adding the Departure Date on which we search for flights
        print ("From: ", from_air, " --> ", "To: ", to_air)
        print()
        print('Please enter your departure date')
        dep_year = input('Year (YYYY): ')
        dep_month = input('Month (MM): ')
        dep_day = input('Day (DD): ')
        if (dep_year == '') or (dep_month == '') or (dep_day == ''):
            dep_year = str(datetime.datetime.now().year)
            dep_month = str(datetime.datetime.now().month).zfill(2)
            dep_day = str(datetime.datetime.now().day).zfill(2)
        url += f"{dep_year}/{dep_month}/{dep_day}"

        # Adding the Api Key and the remaining fields
        url += f'?appId={appID}&appKey={apiKey}&hourOfDay=0&numHours=24&utc=false'
        return url

    elif method.lower() in ["id", "flight_id"]:
        url += "flight/status/"

        # Adding the flight code
        air_code = input('Please Enter the Airline Code (Ex. QR -> Qatar Airways, BA -> British Airways): ').upper()
        flight_no = input('Please Enter the Flight no.: ')
        url += f"{air_code}/{flight_no}/dep/"
        print()
        print('Please enter your departure date')
        dep_year = input('Year (YYYY): ')
        dep_month = input('Month (MM): ')
        dep_day = input('Day (DD): ')
        if (dep_year == '') or (dep_month == '') or (dep_day == ''):
            dep_year = str(datetime.datetime.now().year)
            dep_month = str(datetime.datetime.now().month).zfill(2)
            dep_day = str(datetime.datetime.now().day).zfill(2)
        url += f"{dep_year}/{dep_month}/{dep_day}"

        # Adding the Api Key and the remaining fields
        url += f'?appId={appID}&appKey={apiKey}&utc=false'
        return url

    else:
        try_again = input("Sorry Wrong Input! Do you want to retry? (y/n): ")
        if try_again.lower() in ['y', 'yes']:
            os.system('clear')
            return api_url_generator(host, appID, apiKey)
        else:
            return ""

def airlines(data, code):
    if data.get('appendix', {}).get('airlines'):
        for airline in data['appendix']['airlines']:
            if airline['fs'] == code:
                return airline['name']
    return "Error: Airlines Not Found"

def airport(data, code):
    if data.get('appendix', {}).get('airports'):
        for airport in data['appendix']['airports']:
            if airport['fs'] == code:
                return f"{airport['name']} - {airport['city']}"
    return "Error: No Airports Available"

def strtots(string):
    y = int(string[:4])
    m = int(string[5:7])
    d = int(string[8:10])
    h = int(string[11:13])
    mi = int(string[14:16])
    dt = datetime.datetime(y, m, d, h, mi)
    return time.mktime(dt.timetuple())

def timediff(arr, dep):
    departure = strtots(dep)
    arrival = strtots(arr)
    duration = arrival - departure
    return time.strftime("%H:%M", time.gmtime(duration))

def departed(data):
    print()
    # Actual Departure Time
    ADT = data.get('operationalTimes', {}).get('actualGateDeparture', {}).get('dateLocal', 
        data.get('operationalTimes', {}).get('scheduledGateDeparture', {}).get('dateLocal', 'N/A'))
    ADTime = ADT.split('T')[1].split(':')
    ADTime = f"{ADTime[0]}:{ADTime[1]}"
    print(f'\tActual Departure Time: \t{ADTime}')

    # Time left on journey
    current_time = str(datetime.datetime.utcnow().isoformat())
    UtcSAT = data.get('operationalTimes', {}).get('estimatedGateArrival', {}).get('dateUtc',
        data.get('operationalTimes', {}).get('scheduledGateArrival', {}).get('dateUtc', 'N/A'))
    rem_time = timediff(UtcSAT, current_time)
    rem_time = rem_time.split(':')
    rem_time = f"{rem_time[0]}hrs {rem_time[1]}min"
    print(f'\tArriving at Destination in: \t{rem_time}')

    # Scheduled Arrival Time
    SAT = data.get('operationalTimes', {}).get('scheduledGateArrival', {}).get('dateLocal', 'N/A')
    SATime = SAT.split('T')[1].split(':')
    SATime = f"{SATime[0]}:{SATime[1]}"
    print(f'\tScheduled Arrival Time: \t{SATime}')

def arrived(data):
    print()
    # Actual Departure Time
    ADT = data.get('operationalTimes', {}).get('actualGateDeparture', {}).get('dateLocal', 
        data.get('operationalTimes', {}).get('scheduledGateDeparture', {}).get('dateLocal', 'N/A'))
    ADTime = ADT.split('T')[1].split(':')
    ADTime = f"{ADTime[0]}:{ADTime[1]}"
    print(f'\tActual Departure Time: \t{ADTime}')

    # Actual Arrival Time
    AAT = data.get('operationalTimes', {}).get('actualGateArrival', {}).get('dateLocal', 
        data.get('operationalTimes', {}).get('scheduledGateArrival', {}).get('dateLocal', 'N/A'))
    AATime = AAT.split('T')[1].split(':')
    AATime = f"{AATime[0]}:{AATime[1]}"
    print(f'\tActual Arrival Time: \t{AATime}')

    # Journey Time
    AAT = data.get('operationalTimes', {}).get('actualGateArrival', {}).get('dateUtc', 
        data.get('operationalTimes', {}).get('scheduledGateArrival', {}).get('dateUtc', 'N/A'))
    ADT = data.get('operationalTimes', {}).get('actualGateDeparture', {}).get('dateUtc', 
        data.get('operationalTimes', {}).get('scheduledGateDeparture', {}).get('dateUtc', 'N/A'))
    jour_time = timediff(AAT, ADT)        
    jour_time = jour_time.split(':')
    jour_time = f"{jour_time[0]}hrs {jour_time[1]}min"                                                                                                                                                                                                                                            
    print(f'\tDuration of Journey: \t{jour_time}')

    # Time Since Flight Landed
    current_time = str(datetime.datetime.utcnow().isoformat())
    past_time = timediff(current_time, AAT)
    past_time = past_time.split(':')
    past_time = f"{past_time[0]}hrs {past_time[1]}min"
    print(f'\tTime Since Flight Landed: \t{past_time}')

def scheduled(data):
    print()
    # Scheduled Departure Time
    SDT = data.get('operationalTimes', {}).get('scheduledGateDeparture', {}).get('dateLocal', 'N/A')
    SDTime = SDT.split('T')[1].split(':')
    SDTime = f"{SDTime[0]}:{SDTime[1]}"
    print(f'\tScheduled Departure Time: \t{SDTime}')

    # Scheduled Arrival Time
    SAT = data.get('operationalTimes', {}).get('scheduledGateArrival', {}).get('dateLocal', 'N/A')
    SATime = SAT.split('T')[1].split(':')
    SATime = f"{SATime[0]}:{SATime[1]}"
    print(f'\tScheduled Arrival Time: \t{SATime}')

    # Estimated Journey Begin Time
    current_time = str(datetime.datetime.utcnow().isoformat())
    rem_time = timediff(data.get('operationalTimes', {}).get('scheduledGateDeparture', {}).get('dateUtc', 'N/A'), current_time)
    rem_time = rem_time.split(':')
    rem_time = f"{rem_time[0]}hrs {rem_time[1]}min"
    print(f'\tFlight Departs in: \t{rem_time}')

def output(data):
    statuses = {"A":"Departed", "C":"Canceled", 'D':'Diverted', 'DN':'Data source needed', 'L':'Landed', 'NO':'Not Operational', 'R':'Redirected', 'S':'Scheduled', 'U':'Unknown'}

    if data.get('flightStatuses'):
        print(f"Found {len(data['flightStatuses'])} flight/s for the information provided.")
        print("The Flights Data is presented below: ")
        print("******************************************************************************")
        for flight in data['flightStatuses']:
            print(f"\tFlight No.: \t{flight['carrierFsCode']} {flight['flightNumber']}")
            print(f"\tAirlines: \t{airlines(data, flight['carrierFsCode'])}")
            print()
            print(f"\tFrom: \t{flight['departureAirportFsCode']} \t{airport(data, flight['departureAirportFsCode'])}")
            print(f"\tTo: \t{flight['arrivalAirportFsCode']} \t{airport(data, flight['arrivalAirportFsCode'])}")
            print()
            print(f"\tStatus: \t{statuses.get(flight['status'], 'Unknown')}")
            if statuses.get(flight['status']) == 'Departed':
                departed(flight)
            elif statuses.get(flight['status']) == 'Landed':
                arrived(flight)
            elif statuses.get(flight['status']) == 'Scheduled':
                scheduled(flight)
            print("******************************************************************************")
    else:
        print("Sorry! No Flights found matching your description. Please check all fields and try again :)")

def airport_data_salvager(data):
    airports_path = 'Data/airports.json'
    airports = data.get('appendix', {}).get('airports', [])
    counter = 0
    new_airports = []
    for airport in airports:
        del_fields = ['iata', 'icao', 'localTime', 'classification', 'active', 'delayIndexUrl', 'weatherUrl']
        for field in del_fields:
            airport.pop(field, None)
        airport_name = f"{airport['fs']} - {airport['name']} - {airport['city']}"
        airport['airport'] = airport_name

        if os.path.exists(airports_path):
            airports_data = json.load(open(airports_path, 'r'))
            if airport not in airports_data:
                airports_data.append(airport)
                counter += 1
                new_airports.append(f"{airport['fs']} - {airport['city']}")
            with open(airports_path, "w") as ports_json:
                json.dump(airports_data, ports_json)
        else:
            airports_data = [airport]
            counter += 1
            new_airports.append(f"{airport['fs']} - {airport['city']}")
            with open(airports_path, "w") as ports_json:
                json.dump(airports_data, ports_json)

    if counter > 1:
        print(f"{counter} New airports have been saved to the local storage. They are: ")
    elif counter == 1:
        print(f"{counter} New airport has been saved to the local storage. It is: ")
    else:
        print("No New Airports have been located.")

    if new_airports:
        for i in new_airports:
            print(i)

def airlines_data_salvager(data):
    airlines_path = 'Data/airlines.json'
    airlines = data.get('appendix', {}).get('airlines', [])
    counter = 0
    new_airlines = []
    for flight in airlines:
        del_fields = ['iata', 'icao', 'phoneNumber', 'active']
        for field in del_fields:
            flight.pop(field, None)
        flight_name = f"{flight['fs']} - {flight['name']}"
        flight['airline'] = flight_name

        if os.path.exists(airlines_path):
            airlines_data = json.load(open(airlines_path, 'r'))
            if flight not in airlines_data:
                airlines_data.append(flight)
                counter += 1
                new_airlines.append(flight['airline'])
            with open(airlines_path, "w") as flights_json:
                json.dump(airlines_data, flights_json)
        else:
            airlines_data = [flight]
            counter += 1
            new_airlines.append(flight['airline'])
            with open(airlines_path, "w") as flights_json:
                json.dump(airlines_data, flights_json)

    if counter > 1:
        print(f"{counter} New airlines have been saved to the local storage. They are: ")
    elif counter == 1:
        print(f"{counter} New airline has been saved to the local storage. It is: ")
    else:
        print("No New Airlines have been located.")

    if new_airlines:
        for i in new_airlines:
            print(i)

os.system('clear')
# Creating the API URL 
host = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/"
appID = "c0108d04"
apiKey = "a05ff275a408df68c013da1bc00d4046"

flight_stat_url = api_url_generator(host, appID, apiKey)
os.system('clear')

if flight_stat_url:
    response = requests.get(flight_stat_url)
    data = response.json()
    output(data)
    # Uncomment if you want to save new airport and airline data
    # airport_data_salvager(data)
    # airlines_data_salvager(data)

# Print additional information
try:
    airports_data = json.load(open('Data/airports.json', 'r'))
    print(f"Total No. of airports collected: {len(airports_data)}")
except FileNotFoundError:
    print("No airport data file found.")

# Example Airport Status URL
# airport_url = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/airport/status/ABQ/arr/2018/08/17/22?appId=***&appKey=***&utc=false&numHours=1"
# Airport Status Web Scrapping
# "https://www.flightstats.com/v2/airport-conditions/YKF"









'''
data = {
		 "request": {
			  "airline": {
			   "requestedCode": "AA",
			   "fsCode": "AA"
			  },
			  "flight": {
			   "requested": "100",
			   "interpreted": "100"
			  },
			  "date": {
			   "year": "2018",
			   "month": "8",
			   "day": "20",
			   "interpreted": "2018-08-20"
			  },
			  "utc": {
			   "requested": "false",
			   "interpreted": false
			  },
			  "airport": {},
			  "codeType": {},
			  "extendedOptions": {},
			  "url": "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/AA/100/arr/2018/08/20"
		 },
		 "appendix": {
			  "airlines": [
				   {
				    "fs": "AA",
				    "iata": "AA",
				    "icao": "AAL",
				    "name": "American Airlines",
				    "phoneNumber": "08457-567-567",
				    "active": true
				   },
				   {
				    "fs": "LY",
				    "iata": "LY",
				    "icao": "ELY",
				    "name": "El Al",
				    "phoneNumber": "+ 972-3-9771111",
				    "active": true
				   },
				   {
				    "fs": "AY",
				    "iata": "AY",
				    "icao": "FIN",
				    "name": "Finnair",
				    "phoneNumber": "+ 358 600 140 140",
				    "active": true
				   },
				   {
				    "fs": "IB",
				    "iata": "IB",
				    "icao": "IBE",
				    "name": "Iberia",
				    "phoneNumber": "1800 772 4642",
				    "active": true
				   },
				   {
				    "fs": "BA",
				    "iata": "BA",
				    "icao": "BAW",
				    "name": "British Airways",
				    "phoneNumber": "1-800-AIRWAYS",
				    "active": true
				   },
				   {
				    "fs": "GF",
				    "iata": "GF",
				    "icao": "GFA",
				    "name": "Gulf Air",
				    "phoneNumber": "973 17 335 777",
				    "active": true
				   }
			  ],
			  "airports": [
				   {
				    "fs": "JFK",
				    "iata": "JFK",
				    "icao": "KJFK",
				    "faa": "JFK",
				    "name": "John F. Kennedy International Airport",
				    "street1": "JFK Airport",
				    "city": "New York",
				    "cityCode": "NYC",
				    "stateCode": "NY",
				    "postalCode": "11430",
				    "countryCode": "US",
				    "countryName": "United States",
				    "regionName": "North America",
				    "timeZoneRegionName": "America/New_York",
				    "weatherZone": "NYZ178",
				    "localTime": "2018-08-20T22:39:32.176",
				    "utcOffsetHours": -4,
				    "latitude": 40.642335,
				    "longitude": -73.78817,
				    "elevationFeet": 13,
				    "classification": 1,
				    "active": true,
				    "delayIndexUrl": "https://api.flightstats.com/flex/delayindex/rest/v1/json/airports/JFK?codeType=fs",
				    "weatherUrl": "https://api.flightstats.com/flex/weather/rest/v1/json/all/JFK?codeType=fs"
				   },
				   {
				    "fs": "LHR",
				    "iata": "LHR",
				    "icao": "EGLL",
				    "name": "London Heathrow Airport",
				    "city": "London",
				    "cityCode": "LON",
				    "stateCode": "EN",
				    "countryCode": "GB",
				    "countryName": "United Kingdom",
				    "regionName": "Europe",
				    "timeZoneRegionName": "Europe/London",
				    "localTime": "2018-08-21T03:39:32.176",
				    "utcOffsetHours": 1,
				    "latitude": 51.469603,
				    "longitude": -0.453566,
				    "elevationFeet": 80,
				    "classification": 1,
				    "active": true,
				    "delayIndexUrl": "https://api.flightstats.com/flex/delayindex/rest/v1/json/airports/LHR?codeType=fs",
				    "weatherUrl": "https://api.flightstats.com/flex/weather/rest/v1/json/all/LHR?codeType=fs"
				   }
			  ],
			  "equipments": [
				   {
				    "iata": "77W",
				    "name": "Boeing 777-300ER",
				    "turboProp": false,
				    "jet": true,
				    "widebody": true,
				    "regional": false
				   }
		  		]
		 },
		 "flightStatuses": [
			  {
			   "flightId": 970236480,
			   "carrierFsCode": "AA",
			   "flightNumber": "100",
			   "departureAirportFsCode": "JFK",
			   "arrivalAirportFsCode": "LHR",
			   "departureDate": {
				    "dateLocal": "2018-08-19T18:15:00.000",
				    "dateUtc": "2018-08-19T22:15:00.000Z"
				   },
			   "arrivalDate": {
				    "dateLocal": "2018-08-20T06:20:00.000",
				    "dateUtc": "2018-08-20T05:20:00.000Z"
				   },
			   "status": "L",
			   "schedule": {
				    "flightType": "J",
				    "serviceClasses": "RFJY",
				    "restrictions": ""
				   },
			   "operationalTimes": {
				    "publishedDeparture": {
					     "dateLocal": "2018-08-19T18:15:00.000",
					     "dateUtc": "2018-08-19T22:15:00.000Z"
					    },
				    "publishedArrival": {
					     "dateLocal": "2018-08-20T06:20:00.000",
					     "dateUtc": "2018-08-20T05:20:00.000Z"
					    },
				    "scheduledGateDeparture": {
					     "dateLocal": "2018-08-19T18:15:00.000",
					     "dateUtc": "2018-08-19T22:15:00.000Z"
					    },
				    "estimatedGateDeparture": {
					     "dateLocal": "2018-08-19T18:13:00.000",
					     "dateUtc": "2018-08-19T22:13:00.000Z"
					    },
				    "actualGateDeparture": {
					     "dateLocal": "2018-08-19T18:13:00.000",
					     "dateUtc": "2018-08-19T22:13:00.000Z"
					    },
				    "flightPlanPlannedDeparture": {
					     "dateLocal": "2018-08-19T18:56:00.000",
					     "dateUtc": "2018-08-19T22:56:00.000Z"
					    },
				    "estimatedRunwayDeparture": {
					     "dateLocal": "2018-08-19T18:48:00.000",
					     "dateUtc": "2018-08-19T22:48:00.000Z"
					    },
				    "actualRunwayDeparture": {
					     "dateLocal": "2018-08-19T18:48:00.000",
					     "dateUtc": "2018-08-19T22:48:00.000Z"
					    },
				    "scheduledGateArrival": {
					     "dateLocal": "2018-08-20T06:20:00.000",
					     "dateUtc": "2018-08-20T05:20:00.000Z"
					    },
				    "estimatedGateArrival": {
					     "dateLocal": "2018-08-20T06:11:00.000",
					     "dateUtc": "2018-08-20T05:11:00.000Z"
					    },
				    "actualGateArrival": {
					     "dateLocal": "2018-08-20T06:11:00.000",
					     "dateUtc": "2018-08-20T05:11:00.000Z"
					    },
				    "flightPlanPlannedArrival": {
					     "dateLocal": "2018-08-20T06:11:00.000",
					     "dateUtc": "2018-08-20T05:11:00.000Z"
					    },
				    "estimatedRunwayArrival": {
					     "dateLocal": "2018-08-20T06:05:00.000",
					     "dateUtc": "2018-08-20T05:05:00.000Z"
					    },
				    "actualRunwayArrival": {
					     "dateLocal": "2018-08-20T06:05:00.000",
					     "dateUtc": "2018-08-20T05:05:00.000Z"
					    }
				   },
			   "codeshares": [
				    {
				     "fsCode": "AY",
				     "flightNumber": "4012",
				     "relationship": "L"
				    },
				    {
				     "fsCode": "BA",
				     "flightNumber": "1511",
				     "relationship": "L"
				    },
				    {
				     "fsCode": "GF",
				     "flightNumber": "6654",
				     "relationship": "L"
				    },
				    {
				     "fsCode": "IB",
				     "flightNumber": "4218",
				     "relationship": "L"
				    },
				    {
				     "fsCode": "LY",
				     "flightNumber": "8051",
				     "relationship": "L"
				    }
		   		],
			   "flightDurations": {
				    "scheduledBlockMinutes": 425,
				    "blockMinutes": 418,
				    "scheduledAirMinutes": 375,
				    "airMinutes": 377,
				    "scheduledTaxiOutMinutes": 41,
				    "taxiOutMinutes": 35,
				    "scheduledTaxiInMinutes": 9,
				    "taxiInMinutes": 6
			   },
			   "airportResources": {
				    "departureTerminal": "8",
				    "departureGate": "8",
				    "arrivalTerminal": "3",
				    "arrivalGate": "27",
				    "baggage": "10"
			   },
			   "flightEquipment": {
				    "scheduledEquipmentIataCode": "77W",
				    "tailNumber": "N720AN"
				   }
			  }
		 ]
	  }
'''
