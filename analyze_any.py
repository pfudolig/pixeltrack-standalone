'''Assumed 2 nodes on system and 40 total threads on machine'''

import subprocess
from subprocess import Popen
import sys
import pandas as pd
import argparse
import statistics
import numpy as np
import mplhep as hep
import datetime
import os

timestamp = datetime.datetime.now()
start_path = '/data2/user/pfudolig/pixeltrack-standalone/results/'

parser = argparse.ArgumentParser(description='Serial Information')
parser.add_argument('--serial', '--Serial', dest='serial', action='store_true', help='Pass Serial Library, no arguments')
parser.add_argument('--cuda', '--Cuda', '--CUDA', dest='cuda', action='store_true', help='Pass CUDA Library, no arguments')
parser.add_argument('--alpakaserial', '--AlpakaSerial',dest='alps', action='store_true', help='Pass Alpaka Serial Library, no arguments')
parser.add_argument('--alpakacuda', '--AlpakaCuda', '--AlpakaCUDA', dest='alpc', action='store_true', help='Pass Alpaka CUDA Library, no arguments')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run, default = 20')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process, default = 20000')
parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin, default = 1')
parser.add_argument('--socket', dest='pin', type=int, help='Which sockets to pin, default = 1')
parser.add_argument('--nRuns', dest='runs', type=int, help='Amount of runs to average over, default = 3')
args = parser.parse_args()

if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 20000
if args.gpu:
    gpu = args.gpu
else:
    gpu = 1
if args.pin:
    socket = args.pin
    #if args.pin == 0:
    #    socket = "None"
else:
    socket = 1
if args.runs:
    nRuns = args.runs
else:
    nRuns = 3

'''
#check CPU stream errors
if socket == 1 and nStreams > 20 or socket == 2 and nStreams > 20:
    raise ValueError('One CPU can only run on a maximum of 20 threads')
if socket == 0:
    print('Pinning CPU 1 as default')'''

#check library command errors
passed = [True, True, True, True]
if args.serial:
    cmd = 'serial'
else:
    passed[0] = False
if args.cuda:
    cmd = 'cuda'
else:
    passed[1] = False
if args.alps:
    cmd = 'alps'
else:
    passed[2] = False
if args.alpc:
    cmd = 'alpc'
else:
    passed[3] = False
def check(list):
    '''check if any False values (libraries being passed)'''
    boolean = True
    app = []
    for i in range(len(list)):
        if list[i] == boolean:
            app.append(i)
    if len(app) > 1:
        raise ValueError('Cannot pass multiple libraries at once')
    if not app:
        raise ValueError('Must pass at least one library')
check(passed)


def storeAny(cmd,nStreams,maxEvents,gpu,socket,nRuns):
    '''Create csv files of library output for various stream and event amounts, store and log results'''
    big_time, big_thru, big_str = [], [], []
    big_time_std, big_thru_std, big_time_ave, big_thru_ave = [], [], [], []
    big_ev = []
    want_streams = [1,2,4,8,12,16,20,24,28,32,36,40]
    nstreams_index = want_streams.index(nStreams)
    pick_streams = want_streams[:nstreams_index+1]

    for i in pick_streams:
        time = []
        throughput = []
        streams = []
        
        if cmd == 'serial':
            path = start_path + 'serial_results/'
            for j in range(nRuns):
                if socket == "None":
                    do = "./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_pinNone_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                if socket == 1 or socket == 2:
                    add = "numactl -N " + str(socket-1)
                    do = add + " ./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_pin' + str(socket) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output = p.communicate()
                mystring = str(output)
                parts = mystring.split(' ')
                time.append(float(parts[13]))
                throughput.append(float(parts[16]))
                streams.append(float(parts[5]))
        
        if cmd == 'cuda':
            path = start_path + 'cuda_results/'
            gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
            for j in range(nRuns):
                if socket == "None":
                    do = gpu_cmd + " ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_gpu_' + str(gpu) + '_pinNone_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                if socket == 1 or socket == 2:
                    add = " numactl -N " + str(socket-1)
                    do = gpu_cmd + add + " ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_gpu_' + str(gpu) + '_pin' + str(socket) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output = p.communicate()
                mystring = str(output)
                parts = mystring.split(' ')
                time.append(float(parts[15]))
                throughput.append(float(parts[18]))
                streams.append(float(parts[7]))

        if cmd =='alps':
            path = start_path + 'alps_results/'
            for j in range(nRuns):
                if socket == "None":
                    do = "./alpaka --serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_pinNone_'+ str(nStreams) + 's_' + str(maxEvents) + 'e'
                if socket == 1 or socket == 2:
                    add = "numactl -N " + str(socket-1)
                    do = add + " ./serial --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_pin' + str(socket) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                p = Popen(do, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output = p.communicate()
                mystring = str(output)
                parts = mystring.split(' ')
                time.append(float(parts[27]))
                throughput.append(float(parts[30]))
                streams.append(float(parts[15]))

        if cmd == 'alpc':
            path = start_path + 'alpc_results/'
            gpu_cmd = "CUDA_VISIBLE_DEVICES=" + str(gpu)
            for j in range(nRuns):
                if socket == "None":
                    do = gpu_cmd + " ./alpaka --cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_gpu_' + str(gpu) + '_pinNone_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
                if socket == 1 or socket == 2:
                    add = " numactl -N " + str(socket-1)
                    do = gpu_cmd + add + " ./cuda --numberOfThreads " + str(i) + " --numberOfStreams " + str(i) + " --maxEvents " + str(maxEvents)
                    csv_title = str(nRuns) + cmd + '_gpu_' + str(gpu) + '_pin' + str(socket) + '_' + str(nStreams) + 's_' + str(maxEvents) + 'e'
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

    disabled = input("Cache allocator disabled? (y/n) ")
    if disabled == "y":
        label = "disCache"
        both = input("Asynchronous memory allocator also disabled? (y/n) ")
        if both == "y":
            label = "both"
        if both != "y" and both != "n":
            raise ValueError('Must input y or n')
        csv_title = label + '_' + csv_title + '.csv'
    else:
        csv_title = csv_title + '.csv'
    if disabled != "y" and disabled != "n":
        raise ValueError('Must input y or n')

    csvpath = path + 'csv/'
    if os.path.exists(csvpath):
        print("Saving results to " + csvpath)
        df.to_csv(csvpath + csv_title)
    else:
        print("Creating new directory " + csvpath)
        os.makedirs(csvpath)
        df.to_csv(csvpath + csv_title)
        print("Results saved to new directory")

    logfile = path + cmd + '_log.txt'
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t' + 'Input: ' + do)
        myfile.write('\n')
        myfile.write('\t' + 'Output: ' + path + csv_title)

    return(df)

storeAny(cmd,nStreams,maxEvents,gpu,socket,nRuns) 
