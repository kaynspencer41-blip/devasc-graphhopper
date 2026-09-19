import requests
import urllib.parse

# 1. UI ENHANCEMENT: Define Terminal Colors
class UI:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Base URL for the Routing API
route_url = "https://graphhopper.com/api/1/route?"
key = "c3e6482e-9fb2-410f-8247-de80806a183c" 

def geocoding(location, key):
    while location == "":
        location = input(f"{UI.WARNING}Enter the location again: {UI.RESET}")
        
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
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
            
        # UI ENHANCEMENT: Colored API confirmations
        print(f"{UI.CYAN}Geocoding API URL for {new_loc} (Location Type: {value}){UI.RESET}\n{url}\n")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            # UI ENHANCEMENT: Red error text
            print(f"{UI.RED}Geocode API status: {json_status}\nError message: {json_data['message']}{UI.RESET}")
            
    return json_status, lat, lng, new_loc

while True:
    # 2. UI ENHANCEMENT: Clean, professional application banner
    print(f"\n{UI.BOLD}{UI.BLUE}{'='*65}")
    print(f"{'🚗 GRAPHHOPPER NAVIGATION SYSTEM 🚲':^65}")
    print(f"{'='*65}{UI.RESET}")
    print(f"{UI.CYAN}Available Profiles:{UI.RESET} car, bike, foot")
    print(f"{UI.BLUE}{'-'*65}{UI.RESET}")
    
    profile = ["car", "bike", "foot"]
    vehicle = input(f"{UI.BOLD}Enter a vehicle profile (or 'q' to quit): {UI.RESET}").lower()
    
    if vehicle == "quit" or vehicle == "q":
        print(f"{UI.GREEN}Exiting program. Safe travels!{UI.RESET}")
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print(f"{UI.WARNING}No valid vehicle profile entered. Defaulting to 'car'.{UI.RESET}")
        
    loc1 = input(f"\n{UI.BOLD}Starting Location: {UI.RESET}")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    
    loc2 = input(f"{UI.BOLD}Destination: {UI.RESET}")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            # UI ENHANCEMENT: Formatted summary block
            print(f"\n{UI.BOLD}{UI.GREEN}SUCCESS! Routing API Status: {paths_status}{UI.RESET}")
            print(f"{UI.BLUE}Routing API URL:{UI.RESET}\n{paths_url}\n")
            
            print(f"{UI.BOLD}{UI.HEADER}Trip Summary: {orig[3]} ➔ {dest[3]} ({vehicle}){UI.RESET}")
            print(f"{UI.CYAN}Total Distance:{UI.RESET} {miles:.1f} miles / {km:.1f} km")
            print(f"{UI.CYAN}Total Duration:{UI.RESET} {hr:02d}:{min:02d}:{sec:02d}")
            print(f"{UI.BLUE}{'='*85}{UI.RESET}")
            
            # 3. UI ENHANCEMENT: Turn-by-turn directions converted into a clean table
            print(f"{UI.BOLD}{'Turn-by-Turn Instruction':<55} | {'Km':<10} | {'Miles':<10}{UI.RESET}")
            print(f"{UI.BLUE}{'-'*85}{UI.RESET}")
            
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                km_dist = distance / 1000
                mi_dist = distance / 1000 / 1.61
                
                # Truncate extra-long street names so the table columns don't break alignment
                if len(path) > 53:
                    path = path[:50] + "..."
                    
                print(f"{path:<55} | {km_dist:<10.1f} | {mi_dist:<10.1f}")
            print(f"{UI.BLUE}{'='*85}{UI.RESET}")
        else:
            # UI ENHANCEMENT: Highly visible error blocks
            print(f"\n{UI.RED}{UI.BOLD}ERROR: Routing API Status {paths_status}{UI.RESET}")
            print(f"{UI.RED}Error message: {paths_data['message']}{UI.RESET}")
            print(f"{UI.RED}{'*'*65}{UI.RESET}")
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