import folium
import pandas as pd


# Define Function that calculate radius
def calc_radius(num):
    return float((num * 100) / 400.00)


maps = folium.Map(location=[33.589886, -7.603869], zoom_start=10)
df = pd.read_json("../Lab1/Corona_par_ville")
df = df.values
print(df)

for element in df:
    folium.CircleMarker(
        location=(float(element[2]), float(element[3])),
        radius=calc_radius(element[1]),
        popup=element[0] + ' ' + str(element[1]) + ' Cas',
        color="#FF2D00",
        fill=True,
        fill_color="#FF2D00",
    ).add_to(maps)
    print("this" + str(calc_radius(element[1])))
maps.save("index.html")
