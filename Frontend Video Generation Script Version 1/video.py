from math import isnan
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.ndimage as ndimage
import imageio
from matplotlib import animation, rc

# load the data 

df4 = pd.read_csv("Chicago_Crimes_2012_to_2017.csv",error_bad_lines=False)

frames = [df4]
#df = pd.concat(frames)
df=df4
# convert date strings to (year,month) pairs
locations = df.loc[:,["Date","Latitude","Longitude"]]
dates_as_strings = locations.loc[:,"Date"].values
dates_as_datetime = [ datetime.strptime(string, "%m/%d/%Y %H:%M:%S %p") for string in dates_as_strings ]
months = [ (date.year,date.month) for date in dates_as_datetime ]
locations["Month"] = pd.Series(months, index = df.index)
locations.drop(["Date"], axis=1)

# fix types
locations[["Latitude","Longitude"]] = locations[["Latitude","Longitude"]].apply(pd.to_numeric, errors='coerce')
locations = locations.dropna(how='any') # drop crimes with nan lat-long

# let's select crimes with lat-long in the box (41.6,-87.9) to (42.1,-87.4)
# convert lat-long to pixel indices
locations["Latitude"] = (200*(locations["Latitude"] -41.6)).astype(np.int8)
locations["Longitude"] = (200*(locations['Longitude'] + 87.9)).astype(np.int8)

# in the resolution we chose, chicago is contained in the box with corners (0,0) and (100,100)
index_list = np.concatenate((locations[0 > locations.Latitude].index,
                             locations[locations.Latitude > 99].index,
                             locations[0 > locations.Longitude].index,
                             locations[locations.Longitude > 99].index))
                             
try: 
    locations = locations.drop(index_list)
except KeyError:
    pass

A = np.zeros((204,100,100)) # array to hold counts of crimes by month and location during 2001-2004

for i in range(0,204):  # there are ≈ 2 million entries in locations so this will take a little while
    year_month = (int(2012+i/12),1+i%12)
    month = locations.loc[locations['Month'] == year_month]
    
    for _, row in month.iterrows():
        A[i,row['Latitude'],row['Longitude']] += 1
        
# create the animated plot
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
fig, ax = plt.subplots(figsize =(7,7))

plt.title('Crime in Chicago by month (2012-2017)')
im = ndimage.gaussian_filter(A[0], sigma=.9, order=0) # add smoothing 
heatmap = ax.pcolor(im,cmap='plasma',vmin=0, vmax=200)
y = ax.text(5, 5, "Year: %i"%2012, ha="left", va="center", color="w")
m = ax.text(5, 10, "Month: %s"%months[0], ha="left", va="center", color="w")
plt.colorbar(heatmap,ticks=[])

ax.set_yticks([])
ax.set_xticks([])

def draw_frame(i):
    im = ndimage.gaussian_filter(A[i], sigma=.9, order=0) # add smoothing
    heatmap = ax.pcolor(im,cmap='plasma',vmin=0, vmax=200)
    y.set_text("Year: %i"%(2012+int(i/12)))
    m.set_text("Month: %s"%months[i%12])
    return heatmap,
    
anim = animation.FuncAnimation(fig, draw_frame, frames=204, interval=2, blit=True)
print(anim)


plt.show()
