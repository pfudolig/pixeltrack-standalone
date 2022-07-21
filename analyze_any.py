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
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run, default = 20')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process, default = 10000')
parser.add_argument('--serial', '--Serial', dest='serial', action='store_true', help='Pass Serial Library, no arguments')
parser.add_argument('--cuda', '--Cuda', '--CUDA', dest='cuda', action='store_true', help='Pass CUDA Library, no arguments')
parser.add_argument('--alpakaserial', '--AlpakaSerial',dest='alps', action='store_true', help='Pass Alpaka Serial Library, no arguments')
parser.add_argument('--alpakacuda', '--AlpakaCuda', '--AlpakaCUDA', action='store_true', dest='alpc', help='Pass Alpaka CUDA Library, no arguments')
parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin, default = 1')
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

if args.gpu:
    gpu = args.gpu
else:
    gpu = 1
if args.pin:
    socket = args.pin
else:
    socket = 1

#check CPU stream errors
if socket == 1 and nStreams > 20 or socket == 2 and nStreams > 20:
    raise ValueError('One CPU can only run on a maximum of 20 threads')
if socket == 0:
    print('Pinning CPU 1 as default')

#check library command errors
none = [False, False, False, False]
if args.serial:
    cmd = 'serial_cmd'
else:
    none[0] = True
if args.cuda:
    cmd = 'cuda_cmd'
else:
    none[1] = True
if args.alps:
    cmd = 'alps_cmd'
else:
    none[2] = True
if args.alpc:
    cmd = 'alpc_cmd'
else:
    none[3] = True

def check(list):
    #check if any False values (libraries being passed)
    #if all False all libraries passed, if more than 1 False value multiple libraries passed, if all True no libraries passed
    boolean = False
    app = []
    for i in range(len(list)):
        if list[i] == boolean:
            app.append(i)
    print(app)
    if len(app) > 1:
        raise ValueError('Cannot pass multiple libraries at once')
    if not app:
        raise ValueError('Must pass at least one library')
check(none)


def storeAny(nStreams,maxEvents,cmd,gpu,socket):
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        if cmd == 'serial_cmd':
            path = serialpath + '4ser_pin' + str(socket)
            logfile = serlog
            for j in range(4):
                if socket > 2:
                    do = "./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
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
            path = cudapath + '4cuda_gpu' + str(gpu) + '_pin' + str(socket)
            logfile = cudalog
            for j in range(4):
                gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
                if socket > 2:
                    do = gpu_cmd + " ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
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
            path = alpspath + '4alps_pin' + str(socket)
            logfile = alpslog
            for j in range(4):
                if socket > 2:
                    do = "./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
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
            path = alpcpath + '4alpc_gpu' + str(gpu) + '_pin' + str(socket)
            logfile = alpclog
            for j in range(4):
                gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
                if socket > 2:
                    do = gpu_cmd + " ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
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
    
    d = {'nEvents': big_ev, 'nStreams': big_str, 'time': big_time, 'time_std': big_time_std, 'time_ave': big_time_ave, 'throughput': big_thru, 'tput_std': big_thru_std, 'tput_ave': big_thru_ave}
    df = pd.DataFrame(data=d)
    csv_title = path + '_FromAny_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'
    print(csv_title)
    print(do)
    'f.to_csv(csv_title)
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + 'Input: ' + cmd)
        myfile.write('\n')
        myfile.write('\t' + 'Output: ' + csv_title)
    return(df)

storeAny(nStreams,maxEvents,cmd,gpu,socket)
