import requests
import urllib.parse

# Base URL for the Routing API
route_url = "https://graphhopper.com/api/1/route?"
key = "c3e6482e-9fb2-410f-8247-de80806a183c"  # Requires an active API key from Graphhopper

def geocoding(location, key):
    # Prompt the user again if they leave the input blank
    while location == "":
        location = input("Enter the location again: ")
        
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    # urllib.parse.urlencode safely formats the query string parameters
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    # Ensure the API call was successful and a valid location was found
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        # Handle variations in geographic data formatting (not all cities have a 'state' or 'country' key)
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""
            
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
            
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
            
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        # Null fallback if the location API fails
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
            
    return json_status, lat, lng, new_loc

# Main application loop
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    
    # Allow the user to gracefully exit
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")
        
    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    
    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    # If both locations were successfully geocoded, build the route URL
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")
        
        if paths_status == 200:
            # Convert default meter output to miles/km
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            
            # Convert millisecond output to hours, minutes, and seconds
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            print("Distance Traveled: {:.1f} miles / {:.1f} km".format(miles, km))
            print("Trip Duration: {:02d}:{:02d}:{:02d}".format(hr, min, sec))
            print("=================================================")
            
            # Iterate through the nested JSON "instructions" list to print turn-by-turn text
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=================================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")