"""
This module contains function that create map of locations where films
were filmed based on user's location.
"""
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def read_file(filename: str) -> list:
    """
    Reads data from file and converts it into DataFrame.
    """
    with open(filename, encoding="latin-1") as locations_file:
        content = locations_file.readlines()
    for i in range(len(content)):
        content[i] = content[i].strip()
    content = content[15:]
    content = content[:-1]
    film_name = []
    film_year = []
    film_location = []
    for i in range(len(content)):
        j = 0
        film_name_temp = ''
        while content[i][j] != '(':
            film_name_temp += content[i][j]
            j += 1
        j += 1
        film_name_temp = film_name_temp[:-1]
        film_year_temp = ''
        while content[i][j] != ')':
            film_year_temp += content[i][j]
            j += 1
        j += 1
        if '{' in content[i][j:]:
                while content[i][j] != '}':
                    j += 1
        if film_name_temp == None:
            film_name.append('')
        else:
            film_name.append(film_name_temp)
        if film_year_temp == None:
            film_year.append('')
        else:
            film_year.append(film_year_temp)
        film_location.append(content[i][j:].strip())
    df = pd.DataFrame(list(zip(film_name, film_year, film_location)),\
        columns=["Name", "Year", "Location"])
    return df

def get_coordinates(df, year: str):
    """
    Add column to the given DataFrame which contains coordinates of
all films filmed at given year.
    """
    df = df[df["Year"] == year]
    coordinates = []
    geolocator = Nominatim(user_agent="main.py")
    for i in range(len(df["Location"])):
        df_location = df.iloc[i, 2]
        location = geolocator.geocode(df_location)
        if location == None:
            coordinates.append(0)
        else:
            coordinates.append((location.latitude, location.longitude))
    df["Coordinates"] = coordinates
    df = df[df["Coordinates"] != 0]
    return df


def calculate_distance(df, your_position: tuple):
    """
    Calculates distance between user's and locations of filming.
Returns DataFrames of 10 most close films.
    """
    distance = []
    for i in range(len(df["Coordinates"])):
        coordinates = df.iloc[i, 3]
        distance.append(geodesic(coordinates, your_position).kilometers)
    df["Distance"] = distance
    df = df.sort_values(by=["Distance"])
    df = df[:10]
    return df

def map_creation(df, your_position: tuple):
    """
    Creation of the map.
    """
    map = folium.Map(location=your_position, zoom_start=5)
    for i in range(10):
        name = df.iloc[i, 0]
        df_coordinates = df.iloc[i, 3]
        map.add_child(folium.Marker(location=df_coordinates, popup=name, icon=folium.Icon()))
    return map


if __name__ == "__main__":
    # year = input("Please enter a year you would like to have a map for: ")
    # lat, long_ = input("Please enter your location (format: lat, long): ").split(', ')
    # your_position = (float(lat), float(long_))
    # save_path = input("Please enter a path where you would like to save your map: ")
    year = '2020'
    your_position = (49.817545, 24.023932)
    save_path = 'film_locations.html'
    df = read_file("Lab_2/film_locations/DataStorage/locations.list")
    df = get_coordinates(df, year)
    df = calculate_distance(df, your_position)
    map = map_creation(df, your_position)
    map.save(save_path)
