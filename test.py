import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

timestamp = datetime.datetime.now()

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

    for i in range(1,nStreams+1):
        if cmd == 'serial_cmd':
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

                time = parts[13]
                thru = parts[16]
                str = parts[5]
    print(time)
    print(throughput)

storeAny(nStreams,maxEvents,cmd,gpu,socket,nThreads)