import os
import pandas as pd
from tqdm import tqdm
import re
from pathlib import Path
from config import SCREEN_H,SCREEN_W,ROOT_APPS,GRAPH_TITLE_DEFAULT,IMAGE_PATH,IMAGE_NAME_SUFFIX,IMAGE_NAME_PREFFIX
from makeTreeDir import OUTPUT_CSVTOFCSV,OUTPUT_FCSVTOFGRAPH

PATH_RAW_REAL_EYE = '/home/lordwaif/documents/usecase_andiara/raw/'
SEARCH_DATA_PATH = '/home/lordwaif/documents/eye_leoTree'
FOLDER_GROUPBY = 'groupby'
REGEXP_MAP_WITH_BG = 'V[ií]deo (\d)\.'
PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FOLDER_GROUPBY)

def separateByTarget():
    lista = Path(PATH_RAW_REAL_EYE).glob("*.csv")
    for i in lista:
        data = pd.read_csv(i.__str__())
        data['fixation_point_x'] = data.apply(lambda x : int(x['fixation_point_x']*0.01*SCREEN_W),axis=1)
        data['fixation_point_y'] = data.apply(lambda y : int(y['fixation_point_y']*0.01*SCREEN_H),axis=1)
        participantes = set(list(data['participant_display_name']))
        for j in participantes:
            nome = j
            nome = nome.strip()
            nome = nome.replace(',','').replace(' ','_')
            nomeArquivo = i.parent.parent.joinpath(FOLDER_GROUPBY).joinpath(i.stem+'_'+nome+'.csv')
            aluno = data[data['participant_display_name']==j]
            aluno = aluno[['participant_display_name','fixation_point_x', 'fixation_point_y','fixation_duration_ms']]
            aluno.columns = ['ALUNO','X','Y','MS']
            aluno.to_csv(nomeArquivo,index=False)
        ...

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = PATH_TARGET_GROUP.rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        print(cmd)
        os.popen(cmd=cmd).read()
        bar.update(1)
        #break
    ...
separateByTarget()
execFGraph()