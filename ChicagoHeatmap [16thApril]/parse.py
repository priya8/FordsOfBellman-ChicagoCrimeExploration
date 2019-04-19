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
        try:
            map_data.append([d['primary_type'], d['latitude'], d['longitude']])
        except:
            print("whoops")
    print('created map')
    map1 = folium.Map(location=[float(41.8369), float(-87.6847)], zoom_start=11, tiles='OpenStreetMap', width=1700, height=1000)
    prim_types = []
    for d in map_data:
        color = ''
        if d[0] not in prim_types:
            prim_types.append(d[0])
        print(d[1], d[2], d[0])
        if d[0] == 'NARCOTICS':
            color = '#FFFB00'
            # side = 3
        if d[0] == 'CRIMINAL TRESPASS':
            color = '#0033FF'
            # side = 4
        if d[0] == 'THEFT':
            color = '#07FA18'
            # side = 4
        if d[0] == 'CRIMINAL DAMAGE':
            color = '#FA0707'
            # side = 4
        if d[0] == 'BATTERY':
            color = '#FA0707'
            # side = 5
        if d[0] == 'PROSTITUTION':
            color = '#FF00FF'
            # side = 6
        if d[0] == 'OTHER OFFENSE':
            color = '#0033FF'
            # side = 5
        if d[0] == 'ASSAULT':
            color = '#FA0707'
            # side = 5
        if d[0] == 'ROBBERY':
            color = '#07FA18'
            # side = 4
        if d[0] == 'MOTOR VEHICLE THEFT':
            color = '#07FA18'
            # side = 4
        if d[0] == 'KIDNAPPING':
            color = '#07FA18'
            # side = 5
        if d[0] == 'INTERFERENCE WITH PUBLIC OFFICER':
            color = '#0033FF'
            # side = 4
        if d[0] == 'PUBLIC PEACE VIOLATION':
            color = '#0033FF'
            # side = 4
        if d[0] == 'BURGLARY':
            color = '#07FA18'
            # side = 5
        if d[0] == 'GAMBLING':
            color = '#0033FF'
            # side = 4
        if d[0] == 'WEAPONS VIOLATION':
            color = '#FA0707'
            # side = 5
        if d[0] == 'DECEPTIVE PRACTICE':
            color = '#07FA18'
            # side = 4
        if d[0] == 'SEX OFFENSE':
            color = '#FF00FF'
            # side = 6
        if d[0] == 'INTIMIDATION':
            color = '#FA0707'
            # side = 5
        if d[0] == 'OFFENSE INVOLVING CHILDREN':
            color = '#FF00FF'
            # side = 6
        if d[0] == 'OTHER NARCOTIC VIOLATION':
            color = '#FFFB00'
            # side = 3
        if d[0] == 'ARSON':
            color = '#FA0707'
            # side = 5
        if d[0] == 'HOMICIDE':
            color = '#000000'
            # side = 5
        map1.circle_marker([float(d[1]), float(d[2])], popup=str(d[0]), fill_color=color, line_color=color, radius=200,
                           fill_opacity=0.2)
    map1.create_map(path='chiCrimesCircles.html')


if __name__ == "__main__":
    main()
