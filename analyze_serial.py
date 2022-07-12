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
        nevents.append(float(parts[10]))
        time.append(float(parts[13]))
        throughput.append(float(parts[16]))

    d = {'nevents': nevents, 'time': time, 'throughput': throughput}
    df = pd.DataFrame(data=d)
    #print(df)
    return(df)

#ten_events = storeData(10)
#hundred_events = storeData(100)
#five_hundred_events = storeData(500)


def storeByStream(nStreams,maxEvents):
    '''Loop over inputted number of events to record processing time and throughput of serial processing'''
    time = []
    throughput = []
    streams = nStreams

    for i in range(1,nStreams+1): #exclude 0
        cmd = "./serial --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
        print(cmd)
        #p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #output = p.communicate()
        #mystring = str(output)
        #parts = mystring.split(' ')
        #nevents.append(float(parts[10]))
        #time.append(float(parts[13]))
        #throughput.append(float(parts[16]))

    #d = {'nevents': nevents, 'time': time, 'throughput': throughput}
    #df = pd.DataFrame(data=d)
    #print(df)
    #return(df)

print(storeByStream(10,100))


def plotDF(dataframe):
    '''Plot serial processing data'''
    df_nevents = dataframe['# of Streams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']
    plt.bar(df_nevents,df_time)
    plt.xticks()
    plt.xlabel('Amount of Events Ran Concurrently')
    plt.ylabel('Processing Time of Events (s)') 
    plt.title('Processing Time for ' + str(max(df_nevents)) + ' Events Ran (Serially with 1 Thread)') 
    plt.show() 
    plt.savefig('/afs/cern.ch/user/p/pfudolig/pixeltrack-standalone/time_v_10events.png')

#plotDF(ten_events)


























#make a program that runs make serial for several different types of events
#def runSerial(serial):
#    df = pandas.DataFrame()

#make function that plots outputs dep on # of events being passed through
#have to worry about user security issues?
#child process