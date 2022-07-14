import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse

alpakapath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'

parser = argparse.ArgumentParser(description='Alpaka Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of concurrent events')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
args = parser.parse_args()
if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 5000


def storeByStream(nStreams,maxEvents):
    #Loop over various amount of streams for set number of events to record processing time and throughput
    time = []
    throughput = []
    streams = []
    events = []
#--cuda
    for i in range(1,nStreams+1): #exclude 0
        cmd = "CUDA_VISIBLE_DEVICES=0 numactl -N 0 ./alpaka --cuda --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
        p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = p.communicate()
        mystring = str(output)
        parts = mystring.split(' ')

        time.append(float(parts[38]))
        throughput.append(float(parts[41]))
        streams.append(float(parts[26]))
        events.append(maxEvents)

    d = {'nStreams': streams, 'time': time, 'throughput': throughput, 'nEvents': events}
    df = pd.DataFrame(data=d)
    df.to_csv((alpakapath + 'alpc_' + str(nStreams) + 'streams_' + str(maxEvents) + 'events.csv'))
    #print(df)
    return(df)

user_output = storeByStream(nStreams,maxEvents)
#print(user_output)


def plotTime(dataframe):
    #Plot processing time as a function of amount of streams
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']
    events_val = dataframe['nEvents'].iat[0]

    plt.plot(df_streams,df_time,'o',linestyle='solid')
    plt.xlabel('Amount of Streams')
    plt.ylabel('Time of ' + str(events_val) + ' Events (s)') 
    plt.title('Processing Time of Alpaka CUDA') 

    plt.show() 
    plt.savefig(alpakapath + 'alpc_time_' + str(max(df_streams)) + 'streams_' + str(events_val) + 'events.png')
    plt.close()

plotTime(user_output)


def plotThroughput(dataframe):
    #Plot throughput as a function of amount of streams
    df_streams = dataframe['nStreams']
    df_time = dataframe['time']
    df_throughput = dataframe['throughput']
    events_val = dataframe['nEvents'].iat[0]

    plt.plot(df_streams,df_throughput,'o',linestyle='solid')
    plt.xlabel('Amount of Streams')
    plt.ylabel('Throughput (events/s) (' + str(events_val) + ' events)') 
    plt.title('Throughput of Alpaka CUDA') 

    plt.show() 
    plt.savefig(alpakapath + 'alpc_throughput_' + str(max(df_streams)) + 'streams_' + str(events_val) + 'events.png')
    plt.close()

plotThroughput(user_output)
