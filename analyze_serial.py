import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Serial Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of concurrent events')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
args = parser.parse_args()
if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 1
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 1000


def storeByStream(nStreams,maxEvents):
    '''Loop over inputted number of events to record processing time and throughput of serial processing'''
    time = []
    throughput = []
    streams = []
    events = []

    for i in range(1,nStreams+1): #exclude 0
        cmd = "./serial --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
        p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = p.communicate()
        mystring = str(output)
        parts = mystring.split(' ')
        time.append(float(parts[13]))
        throughput.append(float(parts[16]))
        streams.append(float(parts[5]))
        events.append(maxEvents)

    d = {'nStreams': streams, 'time': time, 'throughput': throughput, 'nEvents': events}
    df = pd.DataFrame(data=d)
    return(df)

user_output = storeByStream(nStreams,MaxEvents)


def plotTime(dataframe):
    '''Plot serial processing data'''
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']
    events_val = dataframe['nEvents'].iat[0]

    plt.scatter(df_streams,df_time,color=c)
    plt.xlabel('Amount of Streams')
    plt.ylabel('Time of' + str(events_val) + ' Events (s)') 
    plt.title('Processing Time for ' + str(max(df_streams)) + ' Streams Ran Concurrently (Serial)') 

    plt.show() 
    plt.savefig('/afs/cern.ch/user/p/pfudolig/pixeltrack-standalone/time_' + str(max(df_streams)) + 'streams.png')

'''
def plotThroughput(dataframe):
    '''Plot serial processing data'''
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']

    plt.bar(df_streams,df_throughput)
    plt.xticks()
    plt.xlabel('Amount of Streams')
    plt.ylabel('Throughput (events/s)') 
    plt.title('Throughput of ' + str(max(df_streams)) + ' Streams Ran Concurrently (Serial)') 

    plt.show() 
    plt.savefig('/afs/cern.ch/user/p/pfudolig/pixeltrack-standalone/throughput_' + str(max(df_streams)) + 'streams.png')

plotTime(user_output)
plotThroughput(user_output)'''









# IGNORE
'''
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

print(storeByEvent(maxEvents))'''
























#make a program that runs make serial for several different types of events
#def runSerial(serial):
#    df = pandas.DataFrame()

#make function that plots outputs dep on # of events being passed through
#have to worry about user security issues?
#child process