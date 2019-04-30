from google.cloud import storage
from pyspark.sql.functions import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import datetime

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]="/usr/bin/python3"


from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Chicago_crime_analysis").getOrCreate()
from pyspark.sql.types import  (StructType,StructField,DateType,BooleanType,DoubleType,IntegerType,StringType,TimestampType)
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

#crimes = spark.read.csv("gs://chic_crime/version1/ccd_sample.csv",header = True,schema = crimes_schema)
crimes = spark.read.csv("Chicago_Crimes_2012_to_2017.csv",header = True,schema = crimes_schema)
print(" The crimes dataframe has {} records".format(crimes.count()))
print(crimes.select("PrimaryType").distinct().show(n = 5))

#1. No of crimes
crime_type_groups = crimes.groupBy('PrimaryType').count()
crime_type_counts = crime_type_groups.orderBy('count', ascending=False)
print(crimes.count())

#2.These are the top 20 most frequent crime types:
#crime_type_counts.show(truncate=False)
counts_pddf = pd.DataFrame(crime_type_counts.rdd.map(lambda l: l.asDict()).collect())
plt.rcParams["figure.figsize"] = [26, 8]
sns.set(style="darkgrid")
sns.set_color_codes("pastel")
type_graph = sns.barplot(x='count', y='PrimaryType', data=counts_pddf)
type_graph.set(ylabel="Primary Type", xlabel="Crimes Record Count")
#plt.show()
out_png = 'plt1.png'
plt.savefig(out_png, dpi=150)

#3.What time of the day are ciminal the busiest?
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
#plt.show()
out_png = 'plt2.png'
plt.savefig(out_png, dpi=150)

#4. How have arrests evolved over the years
crimes = crimes.withColumn('date_time', to_timestamp('date', 'MM/dd/yyyy hh:mm:ss a'))\
       .withColumn('month', trunc('date_time', 'YYYY')) #adding a month column to be able to view stats on a monthly basis
type_arrest_date = crimes.groupBy(['arrest', 'month']).count().orderBy(['month', 'count'], ascending=[True, False])
#type_arrest_date.show(3, truncate=False)
datetime.datetime.now()
datetime.datetime.strftime(datetime.datetime.now(), '%H')
type_arrest_pddf = pd.DataFrame(type_arrest_date.rdd.map(lambda l: l.asDict()).collect())
type_arrest_pddf=type_arrest_pddf.dropna()
type_arrest_pddf['yearpd'] = type_arrest_pddf['month'].apply(lambda dt: datetime.datetime.strftime(pd.Timestamp(dt), '%Y'))
type_arrest_pddf['arrest'] = type_arrest_pddf['arrest'].apply(lambda l: l=='True')
type_arrest_pddf.head(5)
t = type_arrest_pddf['count'] - 20 # np.arange(0.0, 2.0, 0.01)
s = type_arrest_pddf['month']

arrested = type_arrest_pddf[type_arrest_pddf['arrest'] == True]
not_arrested = type_arrest_pddf[type_arrest_pddf['arrest'] == False]
fig, ax = plt.subplots()
ax.plot(arrested['month'], arrested['count'], label='Arrested')
ax.plot(not_arrested['month'], not_arrested['count'], label='Not Arrested')

ax.set(xlabel='Year - 2012-2017', ylabel='Total records',
       title='Year-on-year crime records')
ax.grid(b=True, which='both', axis='y')
ax.legend()
#plt.show()
out_png = 'plt3.png'
plt.savefig(out_png, dpi=150)




#5.where do most crimes take place
crime_location  = crimes.groupBy("LocationDescription").count().collect()
location = [item[0] for item in crime_location]
count = [item[1] for item in crime_location]
crime_location = {"location" : location, "count": count}
crime_location = pd.DataFrame(crime_location)
crime_location = crime_location.sort_values(by = "count", ascending  = False)
crime_location = crime_location.iloc[:20]
myplot = crime_location .plot(figsize = (50,20), kind = "barh", color = "#b35900", width = 0.2,
                               x = "location", y = "count", legend = False)
myplot.invert_yaxis()
plt.xlabel("Number of crimes", fontsize = 28)
plt.ylabel("Crime Location", fontsize = 28)
plt.title("Number of Crimes By Location", fontsize = 36)
plt.xticks(size = 24)
plt.yticks(size = 24)
#plt.show()
out_png = 'plt4.png'
plt.savefig(out_png, dpi=150)


