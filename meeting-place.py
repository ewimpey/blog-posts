"""
This script provides functions to find a point of equal distance from multiple input points, 
get amenities around a given point, and display these points on a map.

Author: Evan Wimpey
Date: 20230712
"""

from geopy.geocoders import OpenCage
import numpy as np
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import folium
from geopy.exc import GeocoderTimedOut
import time
import overpy
import webbrowser


def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two geographic points.

    Parameters:
    coord1, coord2 : tuple of float
        Geographic coordinates (latitude, longitude) of two points.

    Returns:
    distance : float
        Haversine distance between coord1 and coord2 in miles.
    """

    # Radius of the Earth in kilometers
    R = 6371.0

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Convert to miles
    distance = R * c * 0.621371

    return distance

def geocode_address(address, api_key):
    """
    Calculate the latitude and longitude .

    Parameters:
    address : string
        address of point of interest
    api_key : string
        OpenCage API key

    Returns:
    lat,lon : tuple
        Returns lat-lon if availabe in OpenCage.
    """
    geolocator = OpenCage(api_key)
    location = geolocator.geocode(address)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return None
 
def geocode_addresses(addresses, api_key):
    """
    Geocode a list of addresses.

    This function takes a list of addresses in string format and returns a list of
    corresponding geographic coordinates.

    Parameters:
    addresses : list of str
        The addresses to geocode.
    api_key : str
        The API key for the geocoding service.

    Returns:
    coords : list of tuple
        The geographic coordinates of the addresses, as (latitude, longitude) tuples.

    Raises:
    GeocoderTimedOut: If the geocoding service does not respond within the timeout limit.
    """
    coords = []
    for address in addresses:
        coord = geocode_address(address, api_key)
        coords.append(coord)
    return coords


def equal_distance_point(coords, resolution=None):
    """
    Calculate the best point given the input coords.

    Parameters:
    coords : list of tuple
        List of geographic coordinates (latitude, longitude) of the input points.
    resolution : float, optional
        The resolution for the grid search. 

    Returns:
    best_point : tuple of float
        Geographic coordinates (latitude, longitude) of the point that minimizes the 
        maximum Haversine distance to the input points.
    """

    # Define the bounding box
    min_lat = min(coord[0] for coord in coords)
    max_lat = max(coord[0] for coord in coords)
    min_lon = min(coord[1] for coord in coords)
    max_lon = max(coord[1] for coord in coords)

    # Set the default resolution if not provided
    if resolution is None:
        resolution = max((max_lat - min_lat), (max_lon - min_lon)) * 0.01

    lat_values = np.arange(min_lat, max_lat, resolution)
    lon_values = np.arange(min_lon, max_lon, resolution)

    best_point = None
    best_max_distance = None

    for lat in lat_values:
        for lon in lon_values:
            point = (lat, lon)
            distances = [haversine_distance(point, coord) for coord in coords]
            max_distance = max(distances)

            if best_max_distance is None or max_distance < best_max_distance:
                best_point = point
                best_max_distance = max_distance

    return best_point


def create_cp_map(input_coordinates, equal_distance_point):
    """
    Generate a map from the input coordinates and best meeting place.

    Parameters:
    input_coordinates : list of tuple
        List of geographic coordinates (latitude, longitude) of the input points.
    equal_distance_point : tuple
        The ideal meeting spot. 

    Returns:
    m : map
        Map object from the folium package
    """

    # Create a map centered at the equal distance point
    m = folium.Map(location=equal_distance_point, zoom_start=10)

    # Add markers for the input coordinates
    for coord in input_coordinates:
        folium.Marker(coord).add_to(m)

    # Add a marker for the equal distance point
    folium.Marker(equal_distance_point, icon=folium.Icon(color="red")).add_to(m)

    # Display the map
    return m

def get_all_amenities(location, radius=1000):
    """
    Find all amenities within specified radius from a point.

    Parameters:
    location : tuple
        The lat and lon of the ideal meeting spot
    radius : float
        The size of the search radius in meters. 

    Returns:
    amenities : list
        list of all amenities found
    """
    
    lat, lon = location[0], location[1]
    
    api = overpy.Overpass()

    # Define query
    query = f"""
    (
    node["amenity"](around:{radius},{lat},{lon});
    );

    out body;
    """

    try:
        result = api.query(query)  # Added timeout
        print("Query result obtained")  # For debugging
    except Exception as e:
        print("Query failed:", e)  # For debugging
        return []  # Return an empty list if the query fails

    amenities = []
    for node in result.nodes:
        lat = float(node.lat)
        lon = float(node.lon)
        amenity_type = node.tags.get('amenity', 'Unknown')
        name = node.tags.get('name', 'Unnamed')
        street = node.tags.get('addr:street', '')
        house_number = node.tags.get('addr:housenumber', '')
        address = f"{house_number} {street}" if street or house_number else "Unknown"
        amenities.append((lat, lon, amenity_type, name, address))

    print(f"Returning {len(amenities)} amenities")  # For debugging
    return amenities

def get_amenities(amenities, interests = ['restaurant']):
    """
    Subset to amenities of interest.

    Parameters:
    amenities : list
        List of all amenities
    interests : list 
        List of all amenity types of interest. 

    Returns:
    options : dataframe
        pandas dataframe with all relevant amenities
    """
    # turn list into dataframe
    df = pd.DataFrame(amenities, columns=['Latitude', 'Longitude', 'Type', 'Name', 'Address'])
    
    # Filter the DataFrame
    filtered_df = df[df['Type'].isin(interests)]
    
    print(f"Returning {len(filtered_df)} relevant amenities")
    
    return filtered_df

def create_map_with_amenities(input_coordinates, amenities_df, n):
    """
    Create a map showing the input coordinates and potential meeting places.

    Parameters:
    input_coordinates : list of tuple
        List of geographic coordinates (latitude, longitude) of the input points.
    amenities_df : DataFrame
        DataFrame with columns 'Latitude', 'Longitude', and 'Name', containing potential meeting places.
    n : int
        The number of meeting places to display on the map.

    Returns:
    m : folium.Map
        A map showing the input coordinates and the potential meeting places.
    """
    
    # Find the center of all input coordinates
    center_lat = np.mean([lat for lat, lon in input_coordinates])
    center_lon = np.mean([lon for lat, lon in input_coordinates])

    # Create map centered around the center of all input coordinates
    m = folium.Map(location=[center_lat, center_lon], zoom_start=30)

    # Add input coordinates to the map
    for lat, lon in input_coordinates:
        folium.Marker([lat, lon], icon=folium.Icon(color="red")).add_to(m)

    # Add meeting places to the map
    for _, row in amenities_df.head(n).iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], 
                      icon=folium.Icon(color="green"), 
                      popup=row['Name']).add_to(m)

    return m

def find_amenities(addys, api_key, interests, radius=5000, resolution=None):
    """
    Create a map showing the input coordinates and potential meeting places.

    Parameters:
    input_coordinates : list of string
        List of string addresses
    api_key : string
        OpenCage API key
    interests : list of string
        Amenities of interest, from https://wiki.openstreetmap.org/wiki/Key:amenity.

    Returns:
    rel_amenities : dataframe of relevant amenities
        A pandas dataframe of relevant amenities
    """
    
    # turn addresses into coordinates
    coords = geocode_addresses(addys, api_key)

    # find best point
    cp = equal_distance_point(coords, resolution)
    
    # find all amenities within radius
    all_amenities = get_all_amenities(cp, radius)

    # extract only relevant amenities
    rel_amenities = get_amenities(all_amenities, interests)
    
    return rel_amenities, coords

    
# test input params
addys = ["541 Luckie St NW, Atlanta, GA 30313" # Coke Headquarters
         ,"2455 Paces Ferry Road Northwest, Atlanta, GA 30339" # Home Depot
         #,"1030 Delta Blvd, Hapeville, GA 30354" # Delta
         ,"6655 Peachtree Dunwoody Rd, Atlanta, GA 30328" # Newell 
         ,"55 Glenlake Pkwy NE, Atlanta, GA 30328" # UPS
         ]

api_key = "6ce049e5c8dc4935acc2e4027ef790ae"

interests = ['conference_centre', 'events_venue']

# testing for main function
rel_amenities, coords = find_amenities(addys, api_key, interests)

amen_map = create_map_with_amenities(coords, rel_amenities, 5)


### need a way to display the map
amen_map.save('map.html')
webbrowser.open_new_tab("map.html")
###

