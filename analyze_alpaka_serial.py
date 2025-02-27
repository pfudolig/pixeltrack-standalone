import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

alpakapath = '/data2/user/pfudolig/pixeltrack-standalone/results/alps_results/'
logfile = '/data2/user/pfudolig/pixeltrack-standalone/results/alps_results/alps_log.txt'
timestamp = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Alpaka Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run, default = 20')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process, default = 10000')
parser.add_argument('--socket', dest='pin', type=int, help='Which sockets to pin (0 passes as default = 1, args greater than 2 pass as None)')
args = parser.parse_args()
if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 10000
if args.pin:
    socket = args.pin
else:
    socket = 1

if socket == 1 and nStreams > 20 or socket ==2 and nStreams > 20:
    raise ValueError('One CPU can only run on a maximum of 20 threads')
if socket == 0:
    print('Pinning CPU 1 as default')


def storeByStream(nStreams,maxEvents,socket):
    #Loop over various amount of streams for set number of events to record processing time and throughput
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        for j in range(4):
            if socket > 2:
                cmd = "./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
            if socket == 1:
                cmd = "numactl -N 0 ./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
            if socket == 2:
                cmd = "numactl -N 1 ./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
            p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = p.communicate()
            mystring = str(output)
            parts = mystring.split(' ')

            time.append(float(parts[27]))
            throughput.append(float(parts[30]))
            streams.append(float(parts[15]))

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
    csv_title = alpakapath + 'csv/4alps_pin' + str(socket) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'
    df.to_csv(csv_title)
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + 'Input: ' + cmd)
        myfile.write('\n')
        myfile.write('\t' + 'Output: ' + csv_title)
    return(df)

user_output = storeByStream(nStreams,maxEvents,socket)
