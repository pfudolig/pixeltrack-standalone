import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep

cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'

parser = argparse.ArgumentParser(description='Cuda Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of concurrent events')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin')
args = parser.parse_args()
if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 10000
if args.gpu:
    gpu = args.gpu
else:
    gpu = 1


def storeByStream(nStreams,maxEvents,gpu):
    #Loop over various amount of streams for set number of events to record processing time and throughput
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        for j in range(4):
            cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu) + " numactl -N 0 ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
            p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = p.communicate()
            mystring = str(output)
            parts = mystring.split(' ')
            #time = float(parts[7])
            #throughput = parts[18]
            #streams = parts[7]
        #print(mystring)
        #print(time)
        #print(throughput)
        #print(streams)
            time.append(float(parts[15]))
            throughput.append(float(parts[18]))
            streams.append(float(parts[7]))

        time_std = statistics.stdev(time)
        thru_std = statistics.stdev(throughput)
        time_ave = statistics.mean(time)
        thru_ave = statistics.mean(throughput)

        streamval = streams[0]
        big_time.append(time)
        big_thru.append(throughput)
        big_str.append(streamval)
        big_ev.append(maxEvents)

        big_time_std.append(time_std)
        big_thru_std.append(thru_std)
        big_time_ave.append(time_ave)
        big_thru_ave.append(thru_ave)

    d = {'nEvents': big_ev, 'nStreams': big_str, 'time': big_time, 'time_std': big_time_std, 'time_ave': big_time_ave, 'throughput': big_thru, 'tput_std': big_thru_std, 'tput_ave': big_thru_ave}
    df = pd.DataFrame(data=d)
    #df.to_csv('big.csv')
    df.to_csv((cudapath + '4cuda' + str(gpu) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'))
    return(df)
    #print(df)

user_output = storeByStream(nStreams,maxEvents,gpu)
#print(user_output)





'''
def plotThroughput(dataframe,std='NA'):
    #Plot throughput as a function of amount of streams
    df_streams = dataframe['nStreams']
    df_throughput = dataframe['throughput']
    streams_pick = [df_streams[0],df_streams[1],df_streams[3],df_streams[7],df_streams[11],df_streams[15],df_streams[19]]
    thru_std = dataframe['tput_std']
    std_pick = [thru_std[0],thru_std[1],thru_std[3],thru_std[7],thru_std[11],thru_std[15],thru_std[19]]
    thru_ave = dataframe['tput_ave']
    ave_pick = [thru_ave[0],thru_ave[1],thru_ave[3],thru_ave[7],thru_ave[11],thru_ave[15],thru_ave[19]]
    events_val = dataframe['nEvents'].iat[0]

    if std == 'NA':
        plt.style.use(hep.style.CMS)
        plt.figure(figsize = (20,10))
        plt.plot(df_streams,df_throughput,'o',linestyle='solid',label='Cuda')
        plt.legend(loc='lower right',fontsize='xx-small',frameon=True,shadow=True)
        plt.xticks(streams_pick)
        plt.xlabel('Number of Threads/Streams')
        plt.ylabel('Throughput (events/s)') 
        plt.title('Throughput vs. Number of Streams')
        plt.show() 
        plt.savefig(cudapath + 'cudathru_' + str(max(df_streams)) + 's_' + str(events_val) + 'e.png')
        plt.close()

    if std == 'std':
        plt.style.use(hep.style.CMS)
        plt.figure(figsize = (20,10))
        plt.plot(streams_pick,ave_pick,'ro-',linestyle='solid',label='Cuda')
        plt.legend(loc='lower right',fontsize='xx-small',frameon=True,shadow=True)
        plt.xticks(streams_pick,fontsize=16)
        plt.errorbar(streams_pick,ave_pick,yerr=std_pick,fmt='b',ecolor='k',capsize=20, elinewidth=1,markeredgewidth=1)
        plt.xlabel('Number of Threads/Streams',fontsize=16)
        plt.ylabel('Throughput (events/s)',fontsize=16) 
        plt.title('PixelTrack-Standalone Performance',fontsize=20) 
        plt.show() 
        plt.savefig(cudapath + '4ave_cudathru_' + str(max(df_streams)) + 's_' + str(events_val) + 'e.png')
        plt.close()

plotThroughput(user_output,std='std')
'''

