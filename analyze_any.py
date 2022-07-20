import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

serlog = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/serial_log.txt'
cudalog = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/cuda_log.txt'
alpslog = '/data2/user/pfudolig/pixeltrack-standalone/results/alps_results/alps_log.txt'
alpclog = '/data2/user/pfudolig/pixeltrack-standalone/results/alpc_results/alpc_log.txt'
timestamp = datetime.datetime.now()

alpspath = '/data2/user/pfudolig/pixeltrack-standalone/results/alps_results/csv/'
alpcpath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpc_results/csv/'
serialpath = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/csv/'
cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/csv/'

parser = argparse.ArgumentParser(description='Serial Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
parser.add_argument('--serial', '--Serial', dest='serial', help='Pass Serial Library, can type any argument')
parser.add_argument('--cuda', '--Cuda', '--CUDA', dest='cuda', help='Pass CUDA Library, can type any argument')
parser.add_argument('--alpakaserial', '--AlpakaSerial',dest='alps', help='Pass Alpaka Serial Library, can type any argument')
parser.add_argument('--alpakacuda', '--AlpakaCuda', '--AlpakaCUDA', dest='alpc', help='Pass Alpaka CUDA Library, can type any argument')
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

if args.serial:
    cmd = 'serial_cmd'
if args.cuda:
    cmd = 'cuda_cmd'
if args.alps:
    cmd = 'alps_cmd'
if args.alpc:
    cmd = 'alpc_cmd'

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


def storeAny(nStreams,maxEvents,cmd,gpu,socket,nThreads):
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        if cmd == 'serial_cmd':
            path = serialpath
            logfile = serlog
            for j in range(4):
                if socket > 2:
                    do = "./serial --numberOfThreads " + str(nThreads) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
                if socket == 1:
                    do = "numactl -N 0 ./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
                if socket == 2:
                    do = "numactl -N 1 ./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)

                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output = p.communicate()
                mystring = str(output)
                parts = mystring.split(' ')
                time.append(float(parts[13]))
                throughput.append(float(parts[16]))
                streams.append(float(parts[5]))
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
        
        if cmd == 'cuda_cmd':
            path = cudapath
            logfile = cudalog
            for j in range(4):
                gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
                if socket > 2:
                    do = gpu_cmd + " ./cuda --numberOfThreads " + str(nThreads) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                if socket == 1:
                    do = gpu_cmd + " numactl -N 0 ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                if socket == 2:
                    do = gpu_cmd + " numactl -N 1 ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)  

                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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

        if cmd =='alps_cmd':
            path = alpspath
            logfile = alpslog
            for j in range(4):
                if socket > 2:
                    do = "./alpaka --serial --numberOfThreads " + str(nThreads) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
                if socket == 1:
                    do = "numactl -N 0 ./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
                if socket == 2:
                    do = "numactl -N 1 ./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)

                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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

        if cmd == 'alpc_cmd':
            path = alpcpath
            logfile = alpclog
            for j in range(4):
                gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
                if socket > 2:
                    do = gpu_cmd + " ./alpaka --cuda --numberOfThreads " + str(nThreads) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                if socket == 1:
                    do = gpu_cmd + " numactl -N 0 ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                if socket == 2:
                    do = gpu_cmd + " numactl -N 1 ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)  

                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output = p.communicate()
                mystring = str(output)
                parts = mystring.split(' ')
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
    
    print(do)
    print(path)
    print(logfile)

'''
######## Need to generalize this part better
    d = {'nEvents': big_ev, 'nStreams': big_str, 'time': big_time, 'time_std': big_time_std, 'time_ave': big_time_ave, 'throughput': big_thru, 'tput_std': big_thru_std, 'tput_ave': big_thru_ave}
    df = pd.DataFrame(data=d)
    csv_title = path + 'avethrudata_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'
    df.to_csv(csv_title)
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + cmd)
        myfile.write('\n')
        myfile.write('\t' + csv_title)
    return(df)
    #print(df)'''

storeAny(nStreams,maxEvents,cmd,gpu,socket,nThreads)
