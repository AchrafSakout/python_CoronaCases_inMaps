import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy import Nominatim


# Define function that correct cities names
def correct_ville(ville):
    name_ville = []
    for v in ville:
        if v.find(" ") != -1 and v.find("-") != -1:
            # print(i)
            name_ville.append(v.split(sep="-")[1])
        else:
            name_ville.append(v.split(sep=" ")[0].replace("-", " "))
    name_ville[0] = "Casablanca"
    return name_ville


# Define function that correct Cas
def correct_cas(elem):
    cases = []
    for e in elem:
        cases.append(e.replace(',', '.'))
    return cases


# Define function that find lat lng
def geolocator(villes):
    geocodes = []
    geocoder = Nominatim(user_agent="HrfSKT")
    for vi in villes:
        address = geocoder.geocode(vi)
        lnglat = address[1]
        geocodes.append(lnglat)
    return geocodes


# targetPage
page = requests.get("https://sehhty.com/ma-covid/")
# transform to html code
soup = BeautifulSoup(page.content, 'html.parser')
sections = soup.find_all(class_='qa-nav-main')
# getting all city card
casParVille = sections[2].find_all(class_='citycard')
# getting all french city name [1], [0] is for arabic name
ma_villes = [item.find_all(class_='cardlabel')[1].get_text() for item in casParVille]
cas = [item.find(class_='cardcases').get_text() for item in casParVille]
# Correction
ma_villes = correct_ville(ma_villes)
cas = correct_cas(cas)
# Find Lat and Lng
geoCode = geolocator(ma_villes)
laltitude = []
longitude = []
for i in geoCode:
    laltitude.append(i[0])
    longitude.append(i[1])

# making table
tab_villes_cas_geo = pd.DataFrame(
    {
        'ma_villes': ma_villes,
        'cas': cas,
        'lat': laltitude,
        'lng': longitude
    }
)
print(tab_villes_cas_geo)
tab_villes_cas_geo.to_json('Corona_par_ville')

# note
# tab_villes_cas.to_json('Corona_par_villes')
# df=pd.read_json('Corona_par_ma_villes')
# print(df)
