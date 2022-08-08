import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

alpakapath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpc_results/'
logfile = '/data2/user/pfudolig/pixeltrack-standalone/results/alpc_results/alpc_log.txt'
timestamp = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Alpaka Cuda Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run, default = 20')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process, default = 10000')
parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin, default = 1')
parser.add_argument('--socket', dest='pin', type=int, help='Which sockets to pin (0 passes as default = 1, args greater than 2 pass as None)')
parser.add_argument('--disable', dest='disable', type=str, help='Allocator to disable', default = "None")
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
    socket = 1

if socket == 1 and nStreams > 20 or socket == 2 and nStreams > 20:
    raise ValueError('One CPU can only run on a maximum of 20 threads')
if socket == 0:
    print('Pinning CPU 1 as default')

if args.disable:
    alloc = args.disable
else:
    alloc = "None"


def storeByStream(nStreams,maxEvents,gpu,socket,alloc):
    #Loop over various amount of streams for set number of events to record processing time and throughput
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []
    pick = [1,2,4,8,12,16,20]
    
    for i in pick:
        time = []
        throughput = []
        streams = []
        for j in range(3):
            gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
            if socket > 2:
                cmd = gpu_cmd + " ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
            if socket == 1:
                cmd = gpu_cmd + " numactl -N 0 ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
            if socket == 2:
                cmd = gpu_cmd + " numactl -N 1 ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)            
            p = Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = p.communicate()
            mystring = str(output)
            parts = mystring.split(' ')

    print(mystring)
    #print(float(parts[18]))
    #print(float(parts[19]))
    #print(float(parts[10]))

'''
            time.append(float(parts[22]))
            throughput.append(float(parts[25]))
            streams.append(float(parts[10]))

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
    csv_title = alpakapath + 'csv/alpc_g' + str(gpu) + '_pin' + str(socket) + '_dis' + alloc + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'
    df.to_csv(csv_title)
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + 'Input: ' + cmd)
        myfile.write('\n')
        myfile.write('\t' + 'Output: ' + csv_title)
    return(df)'''

user_output = storeByStream(nStreams,maxEvents,gpu,socket,alloc)
