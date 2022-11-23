import os
import pandas as pd
from tqdm import tqdm
import re
from pathlib import Path
from config import SCREEN_H,SCREEN_W,ROOT_APPS,GRAPH_TITLE_DEFAULT,IMAGE_PATH,IMAGE_NAME_SUFFIX,IMAGE_NAME_PREFFIX
from makeTreeDir import OUTPUT_CSVTOFCSV,OUTPUT_FCSVTOFGRAPH

PATH_RAW_REAL_EYE = '/home/lordwaif/documents/usecase_andiara/raw/'
SEARCH_DATA_PATH = '/home/lordwaif/documents/eye_leoTree'
REGEXP_MAP_WITH_BG = 'V[ií]deo (\d)\.'

lista = Path(PATH_RAW_REAL_EYE).glob("*.csv")

for i in lista:
    data = pd.read_csv(i.__str__())
    data['fixation_point_x'] = data.apply(lambda x : int(x['fixation_point_x']*0.01*SCREEN_W),axis=1)
    data['fixation_point_y'] = data.apply(lambda y : int(y['fixation_point_y']*0.01*SCREEN_H),axis=1)
    print(data['participant_display_name'])
    ...
    break

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = Path(PATH_RAW_REAL_EYE).rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        match = re.match(re.compile(REGEXP_MAP_WITH_BG),input.stem)
        bg_command = ''
        titulo = GRAPH_TITLE_DEFAULT
        if match:
            #bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+BG_MAP[input.parts[-3]][int(match.groups()[0])]+IMAGE_NAME_SUFFIX)
            bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+match.groups()[0]+IMAGE_NAME_SUFFIX)
            bg_command = " -bg '"+bg_path+"' "
            #output = Path.joinpath(output.parent,output.stem+output.parts[-4]+"_q"+BG_MAP[input.parts[-3]][int(match.groups()[0])]+output.suffix)
            output = Path.joinpath(output.parent,output.stem+output.parts[-4]+output.suffix)
            #titulo = output.parts[-4]+' Questão '+BG_MAP[input.parts[-3]][int(match.groups()[0])]
            titulo = output.parts[-4]+' ,'+re.sub('V[ií]deo \d\. ','',output.stem).replace('_atv_0_','')
        cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"+bg_command+" -tbg '"+titulo+"'"
        #print(cmd)
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...