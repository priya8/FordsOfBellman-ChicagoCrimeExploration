import requests
import folium


def main():
    url = 'http://data.cityofchicago.org/resource/x2n5-8w5q.json'
    r = requests.get(url)
    data = r.json()
    map_data = []
    for d in data:
        try:
            map_data.append([d['_primary_decsription'], d['latitude'], d['longitude']])
        except KeyError:
            continue
    map1 = folium.Map(location=[float(41.8369), float(-87.6847)], zoom_start=11, tiles='OpenStreetMap', width=1300, height=1000)
    prim_types = []
    for d in map_data:
        color = ''
        if d[0] not in prim_types:
            prim_types.append(d[0])
        if d[0] == 'NARCOTICS':
            color = '#FFFB00'
        if d[0] == 'THEFT':
            color = 'red'
        if d[0] == 'CRIMINAL DAMAGE':
            color = 'blue'
        if d[0] == 'BATTERY':
            color = 'beige'
        if d[0] == 'PROSTITUTION':
            color = 'dark blue'
        if d[0] == 'OTHER OFFENSE':
            color = 'dark blue'
        if d[0] == 'ASSAULT':
            color = 'black'
        if d[0] == 'MOTOR VEHICLE THEFT':
            color = 'pink'
        if d[0] == 'BURGLARY':
            color = 'purple'
        if d[0] == 'DECEPTIVE PRACTICE':
            color = 'dark green'
        folium.CircleMarker(location=[float(d[1]), float(d[2])], color=color, popup=str(d[0]), fill_color=color,fill=True, radius=2,fill_opacity=0.2
                           ).add_to(map1)
    map1.save('C:/Users/semal/Desktop/CU BOULDER SEM 4/BIG DATA ARCHITECTURE/ChicagoHeatmap_16thApril/chiCrimesCircles5.html')


if __name__ == "__main__":
    main()
