import requests
import folium


def main():
    #url = "http://data.cityofchicago.org/resource/ijzp-q8t2.json"
    url = 'http://data.cityofchicago.org/resource/x2n5-8w5q.json'
    r = requests.get(url)
    data = r.json()
    print('Data Type:', type(data))
    print('Length:', len(data))
    map_data = []
    print (data)
    for d in data:
        #print(d)
        try:
            map_data.append([d['_primary_decsription'], d['latitude'], d['longitude']])
        except KeyError:
            continue
    print('created map')
    map1 = folium.Map(location=[float(41.8369), float(-87.6847)], zoom_start=11, tiles='OpenStreetMap', width=1300, height=1000)
    prim_types = []
    for d in map_data:
        color = ''
        if d[0] not in prim_types:
            prim_types.append(d[0])
        print(d[1], d[2], d[0])
        if d[0] == 'NARCOTICS':
            color = '#FFFB00'
            # side = 3
       
            # side = 4
        if d[0] == 'THEFT':
            color = 'red'
            # side = 4
        if d[0] == 'CRIMINAL DAMAGE':
            color = 'blue'
            # side = 4
        if d[0] == 'BATTERY':
            color = 'beige'
            # side = 5
        if d[0] == 'PROSTITUTION':
            color = 'dark blue'
            # side = 6
        if d[0] == 'OTHER OFFENSE':
            color = 'dark blue'
            # side = 5
        if d[0] == 'ASSAULT':
            color = 'black'
            # side = 5
       
            # side = 4
        if d[0] == 'MOTOR VEHICLE THEFT':
            color = 'pink'
            # side = 4
       
            # side = 4
        if d[0] == 'BURGLARY':
            color = 'purple'
            # side = 5
       
            # side = 5
        if d[0] == 'DECEPTIVE PRACTICE':
            color = 'dark green'
            # side = 4
        
            # side = 5
        folium.CircleMarker(location=[float(d[1]), float(d[2])], color=color, popup=str(d[0]), fill_color=color,fill=True, radius=2,fill_opacity=0.2
                           ).add_to(map1)
    map1.save('C:/Users/semal/Desktop/CU BOULDER SEM 4/BIG DATA ARCHITECTURE/ChicagoHeatmap_16thApril/chiCrimesCircles5.html')


if __name__ == "__main__":
    main()
