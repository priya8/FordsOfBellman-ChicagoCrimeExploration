import requests
import folium
import branca.colormap as cm
import branca



def main():
    #url = "http://data.cityofchicago.org/resource/ijzp-q8t2.json"
    url = 'http://data.cityofchicago.org/resource/x2n5-8w5q.json'
    r = requests.get(url)
    data = r.json()
    print('Data Type:', type(data))
    print('Length:', len(data))
    map_data = []
    #print data
    for d in data:
        #print(d)
        try:
            map_data.append([d['_primary_decsription'], d['latitude'], d['longitude']])
        except KeyError:
            continue
        #feature_group=folium.FeatureGroup(name='Narcotics')

        #except:
         #   print("whoops")
    print('created map')
    map1 = folium.Map(location=[float(41.8369), float(-87.6847)], zoom_start=11, tiles='OpenStreetMap', width=1700, height=1000)
    prim_types = []
    option='CRIMINAL DAMAGE'
    for d in map_data:
        color = ''
        
        if d[0] not in prim_types:
            prim_types.append(d[0])

       # print(d[1], d[2], d[0])
        if d[0] == 'NARCOTICS'and option=='NARCOTICS':
            color = '#FFFB00'
          #  group0 = folium.FeatureGroup(name='<span style=\\"color: red;\\">red circles</span>')
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='green' , 
                                                      prefix='fa', icon='circle')))
           # group0.add_to(map1)
           # Coordinate=[float(d[1]), float(d[2])]
           # folium.Marker(location=Coordinate).add_to(feature_group)
            # side = 3
       
            # side = 4
        if d[0] == 'THEFT' and option=='THEFT':
            color = '#07FA18'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='red' , 
                                                      prefix='fa', icon='circle')))
            # side = 4
        if d[0] == 'CRIMINAL DAMAGE' and option=='CRIMINAL DAMAGE':
            color = '#FA0707'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='blue' , 
                                                      prefix='fa', icon='circle')))
            # side = 4
        if d[0] == 'BATTERY' and option=='BATTERY':
            color = '#FA0707'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='blue' , 
                                                      prefix='fa', icon='circle')))
            # side = 5
       
            # side = 6
        if d[0] == 'OTHER OFFENSE' and option=='OTHER OFFENSE':

            color = '#0033FF'
            folium.CircleMarker([float(d[1]), float(d[2])], popup=str(d[0]), fill_color=color , radius=2,
                           fill_opacity=0.2).add_to(map1)
            # side = 5
        if d[0] == 'DECEPTIVE PRACTICE' and option=='DECEPTIVE PRACTICE':

            color = '#07FA18'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='orange' , 
                                                      prefix='fa', icon='circle')))
            
        if d[0] == 'ASSAULT' and option=='ASSAULT':
            color = '#FA0707'
            folium.CircleMarker([float(d[1]), float(d[2])], popup=str(d[0]), fill_color=color , radius=2,
                           fill_opacity=0.2).add_to(map1)
            # side = 5
        if d[0] == 'ROBBERY' and option=='ROBBERY':
            color = '#07FA18'
            folium.CircleMarker([float(d[1]), float(d[2])], popup=str(d[0]), fill_color=color , radius=2,
                           fill_opacity=0.2).add_to(map1)
            # side = 4
        if d[0] == 'MOTOR VEHICLE THEFT' and option=='MOTOR VEHICLE THEFT':
            color = '#07FA18'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='pink' , 
                                                      prefix='fa', icon='circle')))
            # side = 4
        
      
            # side = 4
        if d[0] == 'BURGLARY' and option=='BURGLARY':
            color = '#07FA18'
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='purple' , 
                                                      prefix='fa', icon='circle')))
            # side = 5
        
            # side = 4
       
            # side = 5
      
     
       
     
            # side = 5
      #  map1.CircleMarker()


    #feature_group=FeatureGroup(name='Layer2')



   # map1.add_child(feature_group)    
#    map1.get_root().html.add_child(folium.Element(legend_html))
   # folium.map.LayerControl('topright', collapsed=False).add_to(map1)

    #colormap = cm.linear.Set1.scale(0, 35).to_step(10)
    #colormap.caption = 'A colormap caption'
    #map1.add_child(colormap)
    legend_html = '''
    <div style="position: fixed; 
    top: 50px; right: 50px; width: 100px; height: 90px; 
    border:2px solid grey; z-index:9999; font-size:14px;
    ">&nbsp; Cool Legend <br>
    &nbsp; East &nbsp; <i class="fa fa-map-marker fa-2x"
                  style="color:green"></i><br>
    &nbsp; West &nbsp; <i class="fa fa-map-marker fa-2x" 
                  style="color:red"></i>
    </div>
     '''
    map1.get_root().html.add_child(folium.Element(legend_html))

    map1.save('C:/Users/semal/Desktop/CU BOULDER SEM 4/BIG DATA ARCHITECTURE/Chicago-Crime-Data-master/Chicago-Crime-Data-master/chiCrimesCircles2.html')
 #   map1.create_map(path='chiCrimesCircles.html')


if __name__ == "__main__":
    main()