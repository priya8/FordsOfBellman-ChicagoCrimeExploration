#web/app.py
from flask import Flask,render_template
import requests
import folium
import branca.colormap as cm
import branca
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import  (StructType,StructField,DateType,BooleanType,DoubleType,IntegerType,StringType,TimestampType)
import os
import plotly 
import plotly.io as pio
import plotly.plotly as py
import plotly.graph_objs as go
from pyspark.sql.functions import *
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use(['dark_background'])
import os
import datetime

os.environ["DISPLAY"]="0.0"
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

@app.route('/map-addr', methods=['GET', 'POST'])
def map_call():
    return render_template('map_address.html')

@app.route('/')
def hello():
    return render_template('sampleui.html',name_send6='1') 

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
    return render_template('sampleui.html',values3=count,labels3=location,name_send3='1')

@app.route('/plotdates', methods=['GET', 'POST'])
def crime_date_plot():
    global crimes
    crimes = crimes.withColumn('date_time', to_timestamp('Date', 'MM/dd/yyyy hh:mm:ss a')).withColumn('month', trunc('date_time', 'YYYY')) #adding a month column to be able to view stats on a monthly basis
    df_hour = crimes.withColumn('hour', hour(crimes['date_time']))
    hourly_count = df_hour.groupBy(['PrimaryType', 'hour']).count().cache()
    hourly_total_count = hourly_count.groupBy('hour').sum('count')
    hourly_count_pddf = pd.DataFrame(hourly_total_count.select(hourly_total_count['hour'], hourly_total_count['sum(count)'].alias('count')).rdd.map(lambda l: l.asDict()).collect())
    hourly_count_pddf = hourly_count_pddf.sort_values(by='hour')
    X=hourly_count_pddf['hour']
    y= hourly_count_pddf['count']
    X=X[:-1]
    y=y[:-1]
    return render_template('sampleui.html',values2=y,labels2=X,name_send2='1')


@app.route('/plottypes', methods=['GET', 'POST'])
def crime_type_plot():
    global crimes
    X=[]
    y=[]
    crime_type_groups = crimes.groupBy('PrimaryType').count()
    crime_type_counts = crime_type_groups.orderBy('count', ascending=False)
    counts_pddf = pd.DataFrame(crime_type_counts.rdd.map(lambda l: l.asDict()).collect())
    count_list=counts_pddf.values.tolist()
    for k,v in count_list:
        X.append(k)
        y.append(v)
    return render_template('sampleui.html',values=y,labels=X,name_send4='1')

@app.route('/option/<name>')
def option(name):
    option=name
    print(name)
    file_name="crime"+option+".html"
    return render_template(file_name)
  


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
