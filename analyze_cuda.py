import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'
logfile = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/cuda_log.txt'
timestamp = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Cuda Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of concurrent events')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin')
parser.add_argument('--socket', dest='pin', type=int, help='Which sockets to pin (args greater than 2 pass as None)')
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
if args.pin:
    socket = args.pin
else:
    socket = 3

if nStreams > 20:
    raise ValueError('Only 20 cores on this machine')
if socket == 1 or socket == 2:
    nThreads = nStreams
else:
    nThreads = 40


def storeByStream(nStreams,maxEvents,gpu,socket,nThreads):
    #Loop over various amount of streams for set number of events to record processing time and throughput
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        for j in range(4):
            gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
            if socket > 2:
                cmd = gpu_cmd + " ./cuda --numberOfThreads " + str(nThreads) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
            if socket == 1:
                cmd = gpu_cmd + " numactl -N 0 ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
            if socket == 2:
                cmd = gpu_cmd + " numactl -N 1 ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)            
            p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = p.communicate()
            mystring = str(output)
            parts = mystring.split(' ')
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
    csv_title = cudapath + 'csv/4cuda' + str(gpu) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'
    df.to_csv(csv_title)
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + 'Input: ' + cmd)
        myfile.write('\n')
        myfile.write('\t' + 'Output: ' + csv_title)
    return(df)

user_output = storeByStream(nStreams,maxEvents,gpu,socket,nThreads)