'''Outdated processing-time plotting functions'''

import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep



# SERIAL, just change titles for other libraries
def plotTime(dataframe):
    #Plot processing time as a function of amount of streams
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    events_val = dataframe['nEvents'].iat[0]

    plt.plot(df_streams,df_time,'o',linestyle='solid',label='Serial')
    plt.xlabel('Amount of Streams')
    plt.ylabel('Time of ' + str(events_val) + ' Events (s)') 
    plt.title('Processing Time for Serial') 

    plt.show() 
    plt.savefig(serialpath + 'time_' + str(max(df_streams)) + 'streams_' + str(events_val) + 'events.png')
    plt.close()
plotTime(user_output)



# OVERLAY
def timeOverlay(dataframe1,df1name,dataframe2,df2name):
    #Plot processing data
    df1_streams = dataframe1['nStreams']
    df1_time = dataframe1['time']
    df1_throughput = dataframe1['throughput']
    events_val = dataframe1['nEvents'].iat[0]

    df2_streams = dataframe2['nStreams']
    df2_time = dataframe2['time']
    df2_throughput = dataframe2['throughput']

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(df1_streams,df1_time,c='b',label=df1name)
    ax1.scatter(df2_streams,df2_time,c='r',label=df2name)
    plt.legend(loc='upper right')
    plt.xlabel('Amount of Streams')
    plt.ylabel('Time of ' + str(events_val) + ' Events (s)') 
    plt.title('Times of ' + df1name + ' vs. ' + df2name) 

    plt.show() 
    plt.savefig(respath + df1name + df2name + '_time_' + str(max(df1_streams)) + 'streams_' + str(events_val) + 'events.png')
    plt.close()
timeOverlay(df_serial,'Serial',df_alps,'Alpaka Serial')
timeOverlay(df_cuda,'Cuda',df_alpc,'AlpakaCuda')
