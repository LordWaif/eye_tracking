import argparse
import os
from datetime import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import sys
from config import *

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo txt')

#opcional
parser.add_argument('-o','--output-name', default='output.csv', type=str, required=False, help='nome do arquivo de saida')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']

def sacade(columns_tobe_process=COLUMNS_TO_BE_PROCESS,maxvel=40, maxacc=340,minlen=5):
    df = pd.read_csv(PATH_IN,sep=DEFAULT_SEP_DF)
    axisX = df[columns_tobe_process['X']].values
    axisY = df[columns_tobe_process['Y']].values
    intdist = (np.diff(axisX)**2 + np.diff(axisY)**2)**0.5
    time = df[COLUMN_DATE_TIME].values
    time = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in time])
    time = np.diff(time)
    sec_time = np.array([i.total_seconds() for i in time ])
    vel = intdist/sec_time
    acc = np.diff(vel)
    t0i = 0
    stop = False

    Ssac = [] 
    Esac = []
    
    while not(stop):
        sacstarts = np.where((vel[1+t0i:] > maxvel).astype(int) + (acc[t0i:] > maxacc).astype(int) >= 1)[0]
        if len(sacstarts) > 0:
			# timestamp for starting position
            t1i = t0i + sacstarts[0] + 1
            if t1i >= len(time)-1:
                t1i = len(time)-2
            t1 = time[t1i]
			
			# add to saccade starts
            Ssac.append([t1])
			
			# detect saccade endings
            sacends = np.where((vel[1+t1i:] < maxvel).astype(int) + (acc[t1i:] < maxacc).astype(int) == 2)[0]
            if len(sacends) > 0:
				# timestamp for ending position
                t2i = sacends[0] + 1 + t1i + 2
                if t2i >= len(time):
                    t2i = len(time)-1
                t2 = time[t2i]
                if t2>=t1:
                    dur = t2 - t1
                else:
                    dur = t1 - t2

				# ignore saccades that did not last long enough
                if (dur.total_seconds()*1000) >= minlen:
					# add to saccade ends
                    Esac.append([t1, t2, dur, axisX[t1i], axisY[t1i], axisX[t2i], axisY[t2i]])
                else:
					# remove last saccade start on too low duration
                    Ssac.pop(-1)

				# update t0i
                t0i = 0 + t2i
            else:
                stop = True
        else:
            stop = True
    return Ssac, Esac

if __name__ == '__main__':
    def print_to_stdout(*a):
        # Here a is the array holding the objects
        # passed as the argument of the function
        print(*a, file=sys.stdout)
    ssac,esac = sacade()
    print_to_stdout(len(ssac))