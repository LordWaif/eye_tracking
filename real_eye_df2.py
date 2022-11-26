import os
import pandas as pd
from tqdm import tqdm
import re
from pathlib import Path
from makeTreeDir import cdCreate
import numpy as np

PATH_RAW_REAL_EYE = '/home/lordwaif/documents/usecase_andiara/raw2/'
FOLDER_GROUPBY = 'groupby'
PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FOLDER_GROUPBY)

def separateByTarget():
    lista = Path(PATH_RAW_REAL_EYE).glob("*.csv")
    for i in lista:
        data = pd.read_csv(i.__str__())
        participantes = set(list(data['participant_id']))
        for j in participantes:
            aluno = data[data['participant_id']==j]
            gaze = np.asarray(eval(aluno['test_raw_data'][0]))
            x_gaze = gaze[:,0]
            y_gaze = gaze[:,1]
            ms = gaze[:,2]
            ms = [0]+list(ms)
            ms = np.diff(ms)
            df = pd.DataFrame({'X_TELA':x_gaze,'Y_TELA':y_gaze,'MS':ms})
            df['NOME'] = aluno['participant_tags'][0]
            output = Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').joinpath(i.stem+"_"+aluno['participant_tags'][0]+".csv")
            try:
                df.to_csv(output.__str__())
            except OSError:
                cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').__str__())
                try:
                    df.to_csv(output.__str__())
                except:
                    raise("Não é pra chegar aqui")



def makeDirs(lista):
    cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').__str__())
    for i in lista:
        cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').joinpath(i).__str__())

separateByTarget()