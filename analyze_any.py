import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep

alpakapath = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'
serialpath = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/'
cudapath = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'
respath = '/data2/user/pfudolig/pixeltrack-standalone/results/'

parser = argparse.ArgumentParser(description='Serial Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process')
parser.add_argument('--serial', '--Serial', dest='serial', help='Pass Serial Library, can type any argument')
parser.add_argument('--cuda', '--Cuda', '--CUDA', dest='cuda', help='Pass CUDA Library, can type any argument')
parser.add_argument('--alpakaserial', '--AlpakaSerial',dest='alps', help='Pass Alpaka Serial Library, can type any argument')
parser.add_argument('--alpakacuda', '--AlpakaCuda', '--AlpakaCUDA', dest='alpc', help='Pass Alpaka CUDA Library, can type any argument')
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


def storeAny(nStreams,maxEvents,cmd):
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []

    for i in range(1,nStreams+1):
        time = []
        throughput = []
        streams = []
        if cmd == 'serial_cmd':
            path = '/data2/user/pfudolig/pixeltrack-standalone/results/serial_results/'
            for j in range(4):
                do = "numactl -N 0 ./serial --numberOfStreams " + str(i) + ' --maxEvents ' + str(maxEvents)
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
            path = '/data2/user/pfudolig/pixeltrack-standalone/results/cuda_results/'
            for j in range(4):
                do = "CUDA_VISIBLE_DEVICES=1 numactl -N 0 ./cuda --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
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
            path = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'
            for j in range(4):
                do = "numactl -N 0 ./alpaka --serial --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
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
            path = '/data2/user/pfudolig/pixeltrack-standalone/results/alpaka_results/'
            for j in range(4):
                do = "CUDA_VISIBLE_DEVICES=1 numactl -N 0 ./alpaka --cuda --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
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
    check = [30,31,32,33,34,35,36,37,38,39]
    d = {'check': check,'nEvents': big_ev, 'nStreams': big_str, 'time': big_time, 'time_std': big_time_std, 'time_ave': big_time_ave, 'throughput': big_thru, 'tput_std': big_thru_std, 'tput_ave': big_thru_ave}
    df = pd.DataFrame(data=d)
    #df.to_csv('big.csv')
    df.to_csv((path + 'avethrudata_' + str(nStreams) + 's_' + str(maxEvents) + 'e.csv'))
    #return(df)
    #print(df)

storeAny(nStreams,maxEvents,cmd)