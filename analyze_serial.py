import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def storeByEvent(maxEvents):
    '''Loop over inputted number of events to record processing time and throughput of serial processing'''
    nevents = []
    time = []
    throughput = []

    for i in range(1,maxEvents+1): #exclude 0
        cmd = "./serial --maxEvents " + str(i)
        p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = p.communicate()
        mystring = str(output)
        parts = mystring.split(' ')
        nval = float(parts[10])
        nevents.append(float(parts[10]))
        time.append(float(parts[13]))
        throughput.append(float(parts[16]))

    d = {'nevents': nevents, 'time': time, 'throughput': throughput}
    df = pd.DataFrame(data=d)
    #print(df)
    return(df)

#print(storeByEvent(10))


def storeByStream(nStreams,maxEvents):
    '''Loop over inputted number of events to record processing time and throughput of serial processing'''
    time = []
    throughput = []
    streams = []

    for i in range(1,nStreams+1): #exclude 0
        cmd = "./serial --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
        p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = p.communicate()
        mystring = str(output)
        parts = mystring.split(' ')
        time.append(float(parts[13]))
        throughput.append(float(parts[16]))
        streams.append(float(parts[5]))

    d = {'nStreams': streams, 'time': time, 'throughput': throughput}
    df = pd.DataFrame(data=d)
    #print(df)
    return(df)

ten_streams = storeByStream(10,10)
fthousand_events = storeByStream(20,5000)


def plotDF(dataframe):
    '''Plot serial processing data'''
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']

    plt.bar(df_streams,df_time)
    plt.xticks()
    plt.xlabel('Amount of Streams')
    plt.ylabel('Time of 5000 Events (s)') 
    plt.title('Processing Time for ' + str(max(df_streams)) + ' Streams Ran Concurrently (Serial)') 

    #plt.bar(df_streams,df_throughput)
    #plt.xticks()
    #plt.xlabel('Amount of Streams')
    #plt.ylabel('Throughput (events/s)') 
    #plt.title('Throughput of ' + str(max(df_streams)) + ' Streams Ran Concurrently (Serial)') 

    plt.show() 
    #plt.savefig('/afs/cern.ch/user/p/pfudolig/pixeltrack-standalone/time_v_20s_5000e.png')

plotDF(fthousand_events)


























#make a program that runs make serial for several different types of events
#def runSerial(serial):
#    df = pandas.DataFrame()

#make function that plots outputs dep on # of events being passed through
#have to worry about user security issues?
#child process