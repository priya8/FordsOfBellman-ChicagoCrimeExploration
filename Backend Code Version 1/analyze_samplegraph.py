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

#storage_client=storage.Client()
#bucket=storage_client.get_bucket('chic_crime')
#blobs=list(bucket.list_blobs())
#print(blobs)
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

