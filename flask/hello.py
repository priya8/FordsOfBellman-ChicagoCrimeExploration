from flask import Flask,render_template
import requests
import folium
import branca.colormap as cm
import branca
from pyspark.sql import SparkSession
from pyspark.sql.types import  (StructType,StructField,DateType,BooleanType,DoubleType,IntegerType,StringType,TimestampType)
import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from google.cloud import storage
from pyspark.sql.functions import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use(['dark_background'])
import os
import datetime
import 

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]="/usr/bin/python3"


app = Flask(__name__)
map_count=0
spark = SparkSession.builder.appName("Chicago_crime_analysis").getOrCreate()
crimes_schema = StructType([StructField("_c0", StringType(), True),
                            StructField("ID", StringType(), True),
                            StructField("CaseNumber", StringType(), True),
                            StructField("Date", StringType(), True ),
                            StructField("Block", StringType(), True),
                            StructField("IUCR", StringType(), True),
                            StructField("PrimaryType", StringType(), True  ),
                            StructField("Description", StringType(), True ),
                            StructField("LocationDescription", StringType(), True ),
                            StructField("Arrest", BooleanType(), True),
                            StructField("Domestic", BooleanType(), True),
                            StructField("Beat", StringType(), True),
                            StructField("District", StringType(), True),
                            StructField("Ward", StringType(), True),
                            StructField("CommunityArea", StringType(), True),
                            StructField("FBICode", StringType(), True ),
                            StructField("XCoordinate", DoubleType(), True),
                            StructField("YCoordinate", DoubleType(), True ),
                            StructField("Year", IntegerType(), True),
                            StructField("UpdatedOn", DateType(), True ),
                            StructField("Latitude", DoubleType(), True),
                            StructField("Longitude", DoubleType(), True),
                            StructField("Location", StringType(), True )
                            ])
crimes = spark.read.csv("Chicago_Crimes_2012_to_2017.csv",header = True,schema = crimes_schema)


@app.route('/')
def hello():
    return render_template('sampleui.html') 

@app.route('/2001-2004', methods=['GET', 'POST'])
def one():
    return render_template('2001-2004.html')

@app.route('/2005-2008', methods=['GET', 'POST'])
def two():
    return render_template('2005-2008.html')

@app.route('/2009-2011', methods=['GET', 'POST'])
def three():
    return render_template('2009-2011.html')

@app.route('/2012-2017', methods=['GET', 'POST'])
def four():
    return render_template('2012-2017.html')

@app.route('/plotplaces', methods=['GET', 'POST'])
def crime_loc_plot():
    crime_location  = crimes.groupBy("LocationDescription").count().collect()
    location = [item[0] for item in crime_location]
    count = [item[1] for item in crime_location]
    crime_location = {"location" : location, "count": count}
    crime_location = pd.DataFrame(crime_location)
    crime_location = crime_location.sort_values(by = "count", ascending  = False)
    crime_location = crime_location.iloc[:20]
    myplot = crime_location .plot(figsize = (100,20), kind = "barh", color = "#00ff00", width = 0.8,
                                x = "location", y = "count", legend = False)
    myplot.invert_yaxis()
    plt.xlabel("Number of crimes", fontsize = 50)
    plt.ylabel("Crime Location", fontsize = 50)
    plt.title("Number of Crimes By Location", fontsize = 60)
    plt.xticks(size = 40)
    plt.yticks(size = 40)
    plt.savefig('/home/dharshini/Documents/BDA/Proj-BDA/teams-fords-of-bellman-repositories-1/Frontend Files/flask/static/img/plt1.png', dpi=150)
    plt.close()
    return render_template('sampleui.html',name_send='1',url='/static/img/plt1.png')

@app.route('/plotdates', methods=['GET', 'POST'])
def crime_date_plot():
    global crimes
    crimes = crimes.withColumn('date_time', to_timestamp('Date', 'MM/dd/yyyy hh:mm:ss a')).withColumn('month', trunc('date_time', 'YYYY')) #adding a month column to be able to view stats on a monthly basis
    df_hour = crimes.withColumn('hour', hour(crimes['date_time']))
    hourly_count = df_hour.groupBy(['PrimaryType', 'hour']).count().cache()
    hourly_total_count = hourly_count.groupBy('hour').sum('count')
    hourly_count_pddf = pd.DataFrame(hourly_total_count.select(hourly_total_count['hour'], hourly_total_count['sum(count)'].alias('count')).rdd.map(lambda l: l.asDict()).collect())
    hourly_count_pddf = hourly_count_pddf.sort_values(by='hour')
    fig, ax = plt.subplots()
    ax.plot(hourly_count_pddf['hour'], hourly_count_pddf['count'], label='Hourly Count')
    ax.set(xlabel='Hour of Day', ylabel='Total records',title='Overall hourly crime numbers')
    ax.grid(b=True, which='both', axis='y')
    ax.legend()
    plt.savefig('/home/dharshini/Documents/BDA/Proj-BDA/teams-fords-of-bellman-repositories-1/Frontend Files/flask/static/img/plt2.png', dpi=150)
    plt.close()
    return render_template('sampleui.html',name_send2='1',url2='/static/img/plt2.png')

@app.route('/plottypes', methods=['GET', 'POST'])
def crime_type_plot():
    global crimes
    X=[]
    y=[]
    crime_type_groups = crimes.groupBy('PrimaryType').count()
    crime_type_counts = crime_type_groups.orderBy('count', ascending=False)
    #crime_type_counts.show(truncate=False)
    counts_pddf = pd.DataFrame(crime_type_counts.rdd.map(lambda l: l.asDict()).collect())
    count_list=counts_pddf.values.tolist()
    for k,v in count_list:
        X.append(k)
        y.append(v)
    trace=go.Scatter()
    # plt.rcParams["figure.figsize"] = [50, 10]
    # sns.set(style="darkgrid")
    # sns.set_color_codes("pastel")
    # type_graph = sns.barplot(x='count', y='PrimaryType', data=counts_pddf)
    # type_graph.set(ylabel="Primary Type", xlabel="Crimes Record Count")
    # plt.savefig('/home/dharshini/Documents/BDA/Proj-BDA/teams-fords-of-bellman-repositories-1/Frontend Files/flask/static/img/plt3.png', dpi=150)
    # plt.close()
    # return render_template('sampleui.html',name_send3='1',url3='/static/img/plt3.png')
    return "OK"


@app.route('/option/<name>')
def option(name):
    url = 'http://data.cityofchicago.org/resource/x2n5-8w5q.json'
    r = requests.get(url)
    data = r.json()
    map_data = []
    #print data
    for d in data:
        #print(d)
        try:
            map_data.append([d['_primary_decsription'], d['latitude'], d['longitude']])
        except KeyError:
            continue
    map1 = folium.Map(location=[float(41.8369), float(-87.6847)], zoom_start=11, tiles="Open Street Map", width=1700, height=1000)
    prim_types = []
    option=name
    print(name)
    for d in map_data:
        color = ''
        
        if d[0] not in prim_types:
            prim_types.append(d[0])

       # print(d[1], d[2], d[0])
        if d[0] == 'NARCOTICS'and option=='NARCOTICS':
          #  group0 = folium.FeatureGroup(name='<span style=\\"color: red;\\">red circles</span>')
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='green' , 
                                                      prefix='fa', icon='circle')))
       
            # side = 4
        if d[0] == 'THEFT' and option=='THEFT':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='red' , 
                                                      prefix='fa', icon='circle')))
            # side = 4
        if d[0] == 'CRIMINAL DAMAGE' and option=='CRIMINAL DAMAGE':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='blue' , 
                                                      prefix='fa', icon='circle')))
            # side = 4
        if d[0] == 'BATTERY' and option=='BATTERY':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='beige' , 
                                                      prefix='fa', icon='circle')))
            # side = 5
       
            # side = 6
        if d[0] == 'OTHER OFFENSE' and option=='OTHER OFFENSE':

            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='darkblue' , 
                                                      prefix='fa', icon='circle')))
            # side = 5
        if d[0] == 'DECEPTIVE PRACTICE' and option=='DECEPTIVE PRACTICE':

            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='darkgreen' , 
                                                      prefix='fa', icon='circle')))
            
        if d[0] == 'ASSAULT' and option=='ASSAULT':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='black' , 
                                                      prefix='fa', icon='circle')))
      
            # side = 5
        if d[0] == 'ROBBERY' and option=='ROBBERY':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='orange' , 
                                                      prefix='fa', icon='circle')))

       
            # side = 4
        if d[0] == 'MOTOR VEHICLE THEFT' and option=='MOTOR VEHICLE THEFT':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='pink' , 
                                                      prefix='fa', icon='circle')))
        if d[0] == 'BURGLARY' and option=='BURGLARY':
            map1.add_child(folium.Marker(location=[float(d[1]), float(d[2])],
                                    popup=str(d[0]),
                                    icon=folium.Icon(color='purple' , 
                                                      prefix='fa', icon='circle')))
    global map_count
    map_count+=1
    file_name="crime"+str(map_count)+".html"
    #open('/home/dharshini/Documents/BDA/Proj-BDA/teams-fords-of-bellman-repositories-1/Frontend Files/flask/templates/crime.html','w').close()	
    map1.save('/home/dharshini/Documents/BDA/Proj-BDA/teams-fords-of-bellman-repositories-1/Frontend Files/flask/templates/'+file_name)
    return render_template(file_name)
 #   map1.create_map(path='chiCrimesCircles.html')


if __name__ == '__main__':
    app.run()
