# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:50:24 2015
find out turtle which in ctdWithModTempByDepth.csv is in same area with 4-seconds turtle.
output 12487_location.csv
@author: zdong
"""
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime
def Closest_time(time,time_list):
    'find index of closest time'
    T=[]
    for i in time:
        a=min(time_list, key=lambda t: abs(i - t))
        T.append(a)
    indx=[]
    for i in T:
        a=time_list[time_list==i].index[0]
        indx.append(a)
    return indx
#####################################################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsturtle_id=pd.Series(obsData['PTT'][tf_index],index=tf_index)

secondData=pd.read_csv('turtle_12487_tdr.csv')
time=pd.Series(secondData['Date'])
depth=pd.Series(secondData['Depth'])
temp=pd.Series(secondData['temp'])

indx=[]
for i in tf_index:
    if obsturtle_id[i]==118905:  #this turtle is same turtle with 4-second turtle
        indx.append(i)
obsLon, obsLat = obsData['LON'][indx], obsData['LAT'][indx]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][indx]), index=indx)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][indx]), index=indx)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][indx]), index=indx)

INDX=[]
for i in secondData.index[0:2200000]:   #after 2200000,time is > 2014 
    time[i]=datetime.strptime(time[i], "%Y/%m/%d %H:%M:%S")  # change str to datatime
    if time[i].year==2013:
        if time[i].month==5:
            if time[i].day>22:
                INDX.append(i)
        if 5<time[i].month<9:
            INDX.append(i)        #get in same time
    if i%100000==0:   
        print(i)

closest_indx=Closest_time(time[INDX],obsTime)    #get index of the nearest time in telemetered file. 
lons,lats,Index,INDEX=[],[],[],[]
for i in range(len(closest_indx)):
    if abs((obsTime[closest_indx[i]]-time[i]).total_seconds()/3600)<3:  #the time difference smaller than 3 hours 
        lons.append(obsLon[closest_indx[i]])
        lats.append(obsLat[closest_indx[i]])
        Index.append(closest_indx[i])
        INDEX.append(i)
    if i%100000==0:   
        print(i)
Data=pd.DataFrame(INDX,index=INDX)
Data['time']=pd.Series(time[INDX])
Data['depth']=pd.Series(depth[INDX])
Data['temp']=pd.Series(temp[INDX])
Data['lon']=pd.Series(lons,index=INDEX)
Data['lat']=pd.Series(lats,index=INDEX)   
Data['index']=pd.Series(Index,index=INDEX)
Data.to_csv('12487_location_new.csv')  
