import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
from matplotlib import gridspec
'''
parser = argparse.ArgumentParser(description='Plot Arguments Information')
parser.add_argument('--serial', dest='nstreams', type=int, help='First Dataframe to pass, usually Serial data')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Second Dataframe to pass, usually CUDA data')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Third Dataframe to pass, usually Alpaka data')
args = parser.parse_args()
if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 10000'''


alpakapath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'
serialpath = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/'
cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'
respath = '/data2/user/pfudolig/pixeltrack-standalone/results/'
df_alps = pd.read_csv(alpakapath + '4alps_20s_5e.csv')
df_ser = pd.read_csv(serialpath + '4serial_20s_5e.csv')
df_cuda = pd.read_csv(cudapath + '4cuda_20s_5e.csv')

def ratio_and_std(dataframe1,dataframe2):
    big_ratio, big_std = [], []
    thru_ave1 = dataframe1['tput_ave']
    thru_ave2 = dataframe2['tput_ave']
    thru1 = dataframe1['throughput']
    thru2 = dataframe2['throughput']
    for i in range(len(thru_ave1)):
    #    ratio = thru2 / thru1
    #    print(ratio)
        std_ratio = statistics.stdev(ratio)
        #big_std.append(std_ratio)
        #print(std_ratio)
    #print(big_std)
ratio_and_std(df_ser,df_cuda)

'''
def overlayThru(dataframe1,df1name,dataframe2,df2name,dataframe3,df3name):
    #Usually df1=serial, df2=cuda, df3=alpakaserial
    df_streams1 = dataframe1['nStreams']
    df_throughput1 = dataframe1['throughput']
    streams_pick1 = [df_streams1[0],df_streams1[1],df_streams1[3],df_streams1[7],df_streams1[11],df_streams1[15],df_streams1[19]]
    thru_std1 = dataframe1['tput_std']
    std_pick1 = [thru_std1[0],thru_std1[1],thru_std1[3],thru_std1[7],thru_std1[11],thru_std1[15],thru_std1[19]]
    thru_ave1 = dataframe1['tput_ave']
    ave_pick1 = [thru_ave1[0],thru_ave1[1],thru_ave1[3],thru_ave1[7],thru_ave1[11],thru_ave1[15],thru_ave1[19]]
    events_val1 = dataframe1['nEvents'].iat[0]

    df_streams2 = dataframe2['nStreams']
    df_throughput2 = dataframe2['throughput']
    streams_pick2 = [df_streams2[0],df_streams2[1],df_streams2[3],df_streams2[7],df_streams2[11],df_streams2[15],df_streams2[19]]
    thru_std2 = dataframe2['tput_std']
    std_pick2 = [thru_std2[0],thru_std2[1],thru_std2[3],thru_std2[7],thru_std2[11],thru_std2[15],thru_std2[19]]
    thru_ave2 = dataframe2['tput_ave']
    ave_pick2 = [thru_ave2[0],thru_ave2[1],thru_ave2[3],thru_ave2[7],thru_ave2[11],thru_ave2[15],thru_ave2[19]]
    events_val2 = dataframe2['nEvents'].iat[0]

    df_streams3 = dataframe3['nStreams']
    df_throughput3 = dataframe3['throughput']
    streams_pick3 = [df_streams3[0],df_streams3[1],df_streams3[3],df_streams3[7],df_streams3[11],df_streams3[15],df_streams3[19]]
    thru_std3 = dataframe3['tput_std']
    std_pick3 = [thru_std3[0],thru_std3[1],thru_std3[3],thru_std3[7],thru_std3[11],thru_std3[15],thru_std3[19]]
    thru_ave3 = dataframe3['tput_ave']
    ave_pick3 = [thru_ave3[0],thru_ave3[1],thru_ave3[3],thru_ave3[7],thru_ave3[11],thru_ave3[15],thru_ave3[19]]
    events_val3 = dataframe3['nEvents'].iat[0]
    
    ratio1 = thru_ave2 / thru_ave1
    ratio13_pick = [ratio1[0],ratio1[1],ratio1[3],ratio1[7],ratio1[11],ratio1[15],ratio1[19]]
    ratio2 = thru_ave3 / thru_ave1
    ratio23_pick = [ratio2[0],ratio2[1],ratio2[3],ratio2[7],ratio2[11],ratio2[15],ratio2[19]]


    plt.style.use(hep.style.CMS)
    plt.figure(figsize = (20,10))

    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    fig = plt.subplots(2)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1],sharex=ax1)


    ax1.plot(streams_pick1,ave_pick1,'ro',markersize=7,label=df1name)
    ax1.plot(streams_pick2,ave_pick2,'b^',markersize=7,label=df2name)
    ax1.plot(streams_pick3,ave_pick3,'gs',markersize=7,label=df3name)
    ax1.legend(loc='center',fontsize='xx-small',frameon=True,shadow=True)
    ax1.set(ylabel='Throughput (events/s)',title='PixelTrack-Standalone Performance') 

    ax2.plot(streams_pick1,ratio13_pick,'rP',markersize=10,label=df2name + ' : ' + df1name)
    ax2.plot(streams_pick1,ratio23_pick,'bd',markersize=10,label=df3name + ' : ' + df1name)
    plt.axhline(y=1,linewidth=2,linestyle='dashed',color='g')
    plt.xticks(streams_pick2)
    ax2.tick_params(axis='y',labelsize=16)
    ax2.legend(loc='center',fontsize='xx-small',frameon=True,shadow=True)
    ax2.set_xlabel('Number of Threads/Streams')
    ax2.set_ylabel('Throughput Ratio',fontsize=25)
    ax2.set_ylim(-1,10)

    plt.subplots_adjust(hspace=.0)
    plt.show() 
    plt.savefig(respath + 'thruandratio_' + str(max(df_streams1)) + 's_' + str(events_val1) + 'e.png')
    plt.close()


overlayThru(df_ser,'Serial',df_cuda,'CUDA',df_alps,'AlpakaSerial')'''
