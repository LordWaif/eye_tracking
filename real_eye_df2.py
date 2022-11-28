import os
import pandas as pd
from tqdm import tqdm
import re
from pathlib import Path
from makeTreeDir import cdCreate,OUTPUT_TXTTOCSV,OUTPUT_CSVTOFCSV,OUTPUT_FCSVTOFGRAPH
import numpy as np
from config import COLUMNS_TO_BE_PROCESS,ROOT_APPS

PATH_RAW_REAL_EYE = '/home/lordwaif/documents/usecase_andiara/raw2/'
FOLDER_GROUPBY = 'groupby'
FIXACION_MY = 'csv_fixacion'
#PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FOLDER_GROUPBY)
PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FIXACION_MY)

def separateByTarget(columns_to_be_process=COLUMNS_TO_BE_PROCESS):
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
            df = pd.DataFrame({columns_to_be_process['X']:x_gaze,columns_to_be_process['Y']:y_gaze,'MS':ms})
            df['NOME'] = aluno['participant_tags'][0]
            df[columns_to_be_process['C']] = 1
            output = Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').joinpath(i.stem+"_"+aluno['participant_tags'][0]+".csv")
            try:
                df.to_csv(output.__str__(),index=False)
            except OSError:
                cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').__str__())
                try:
                    df.to_csv(output.__str__(),index=False)
                except:
                    raise("Não é pra chegar aqui")

def execFixacao():
    os.chdir(ROOT_APPS)
    lista = list(Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').glob("*.csv"))
    bar = tqdm(total=len(lista),desc="run_task={}".format('gerando fixações'))
    for i in lista:
        #df = pd.read_csv(i.__str__())
        #input = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
        input = i.__str__()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOFCSV,i.stem+'.csv')
        print(output)

        cmd = "python3 fixacao_real_eye.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        #print(input)
        #print("fixacao.py"+output2.__str__()+'\n')
        print(os.popen(cmd=cmd).read())
        bar.update(1)

def makeDirs(lista):
    cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').__str__())
    for i in lista:
        cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').joinpath(i).__str__())

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = PATH_TARGET_GROUP.rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        #print(input)
        #print(output)
        cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        print(os.popen(cmd=cmd).read())
        #os.popen(cmd=cmd).read()
        bar.update(1)
        #break

#separateByTarget()
#execFixacao()
execFGraph()