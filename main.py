import folium
import pandas as pd
import geopy


map = folium.Map(tiles="Stamen Terrain", location=[49.817545, 24.023932], zoom_start=17)
map.save("../../film_locations.html")


def read_file(filename: str) -> list:
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
print(read_file("locations.list"))