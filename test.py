import subprocess
from subprocess import Popen
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import statistics
import mplhep as hep
import datetime

parser = argparse.ArgumentParser(description='Serial Information')
parser.add_argument('--numberOfStreams', dest='nstreams', type=int, help='Number of streams to run, default = 20')
parser.add_argument('--maxEvents', dest='nEvents', type=int, help='Number of events to process, default = 10000')
parser.add_argument('--serial', '--Serial', dest='serial', action='store_true', help='Pass Serial Library, can type any argument')
parser.add_argument('--cuda', '--Cuda', '--CUDA', dest='cuda', action='store_true', help='Pass CUDA Library, can type any argument')
parser.add_argument('--alpakaserial', '--AlpakaSerial',dest='alps', action='store_true', help='Pass Alpaka Serial Library, can type any argument')
#parser.add_argument('--alpakacuda', '--AlpakaCuda', '--AlpakaCUDA', dest='alpc', help='Pass Alpaka CUDA Library, can type any argument')
#parser.add_argument('--GPU', dest='gpu', type=int, help='GPU Device to pin, default = 1')
#parser.add_argument('--socket', dest='pin', type=int, help='Which sockets to pin (0 passes as default = 1, args greater than 2 pass as None)')
args = parser.parse_args()


if args.nstreams:
    nStreams = args.nstreams
else:
    nStreams = 20
if args.nEvents:
    maxEvents = args.nEvents
else:
    maxEvents = 10000

none = [False, False, False]
#if all false, all libraries being passed
#if all true, no libraries being passed

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

def check(list):
    #check if any False values (libraries being passed)
    #if all False, all libraries passed
    #if more than 1 False value, multiple libraries passed
    #if all True, no libraries passed
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

'''
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
    print('Pinning CPU 1 as default')'''