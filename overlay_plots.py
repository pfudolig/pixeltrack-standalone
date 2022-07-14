import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse

serialpath = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/'
cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'
alpath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'
respath = '/data2/user/pfudolig/pixeltrack-standalone/results/'

#f_serial = pd.read_csv(serialpath + 'serial_20streams_5000.events.csv')
df_cuda = pd.read_csv(cudapath + 'parallel_20streams_5000events.csv')
#df_alps = pd.read_csv(alpath + 'alps_20streams_5000events.csv')
df_alpc = pd.read_csv(alpath + 'alpc_20streams_5000events.csv')


def plotTime(dataframe1,df1name,dataframe2,df2name):
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

#plotTime(df_serial,'Serial',df_alps,'Alpaka Serial')
plotTime(df_cuda,'Cuda',df_alpc,'AlpakaCuda')


def plotThroughput(dataframe1,df1name,dataframe2,df2name):
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
    ax1.scatter(df1_streams,df1_throughput,c='b',label=str(df1name))
    ax1.scatter(df2_streams,df2_throughput,c='r',label=str(df2name))
    plt.legend(loc='upper right')
    plt.xlabel('Amount of Streams')
    plt.ylabel('Throughput (events/s) (' + str(events_val) + ' events)') 
    plt.title('Throughputs of ' + df1name + ' vs. ' + df2name) 

    plt.show() 
    plt.savefig(respath + df1name + df2name + '_throughput_' + str(max(df1_streams)) + 'streams_' + str(events_val) + 'events.png')
    plt.close()

#plotThroughput(df_serial,'Serial',df_alps,'AlpakaSerial')
plotThroughput(df_cuda,'Cuda',df_alpc,'AlpakaCuda')