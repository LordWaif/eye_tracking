import os
import pandas as pd
from tqdm import tqdm
import re
from pathlib import Path
from makeTreeDir import cdCreate,OUTPUT_TXTTOCSV,OUTPUT_CSVTOFCSV,OUTPUT_FCSVTOFGRAPH
import numpy as np
from config import COLUMNS_TO_BE_PROCESS,ROOT_APPS,OUTLIER,SCREEN_W,SCREEN_H
#from math import isnan

GROUPS = dict()
GROUPS['soma_2'] = (['davi','enzo','gabriel','leonardo','rafael yuri'],'soma2.png')
GROUPS['contagem_e_soma_material_completo'] = (['davi','enzo','gabriel','leonardo','rafael yuri'],'soma_material_concreto.png')

GROUPS['adicao_robo'] = (['alice','luis otavio','nicolle','pedro felipe','robert','theo','wenzo'],'adicao_robo.png')
GROUPS['adicao_baixa_acessibilidade'] = (['alice','luis otavio','nicolle','pedro felipe','robert','theo','wenzo'],'adicao_baixa_acessibilidade.png')

GROUPS['contagem_passaro'] = (['arthur','gael','joão victor','maria helena'],'contagem_passaro.png')
GROUPS['contagem_e_soma_material_completo'] = (['arthur','gael','joão victor','maria helena'],'contagem_material_concreto.png')

PATH_RAW_REAL_EYE = '/home/lordwaif/documents/usecase_andiara/raw2/'
FOLDER_GROUPBY = 'groupby'
FIXACION_MY = 'csv_fixacion'
#PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FOLDER_GROUPBY)
PATH_TARGET_GROUP = Path(PATH_RAW_REAL_EYE).parent.joinpath(FIXACION_MY)
PATH_TARGET_HEAT_INPUT = Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos')
INPUT_CSVTOCSVHEAT = 'csv_heat_input'

def separateByTarget(columns_to_be_process=COLUMNS_TO_BE_PROCESS):
    lista = Path(PATH_RAW_REAL_EYE).glob("*.csv")
    for i in lista:
        data = pd.read_csv(i.__str__())
        #data = data[data['participant_tags'].fillna(0)]
        data['participant_tags'] = data['participant_tags'].fillna('desconhecido')
        participantes = set(list(data['participant_id']))
        #print(data['participant_tags'])
        for j in participantes:
            aluno = data[data['participant_id']==j]
            gaze = np.asarray(eval(aluno['test_raw_data'].iloc[0]))
            x_gaze = gaze[:,0]
            y_gaze = gaze[:,1]
            ms = gaze[:,2]
            #print(ms[0:10])
            ms = [0]+list(ms)
            ms = np.diff(ms)
            delete_index = np.where(ms>OUTLIER)
            x_gaze = np.delete(x_gaze,delete_index,0)
            y_gaze = np.delete(y_gaze,delete_index,0)
            ms = np.delete(ms,delete_index,0)
            df = pd.DataFrame({columns_to_be_process['X']:x_gaze,columns_to_be_process['Y']:y_gaze,'MS':ms})
            df['NOME'] = aluno['participant_tags'].iloc[0]
            df[columns_to_be_process['C']] = 1
            output = Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').joinpath(i.stem+"_"+aluno['participant_tags'].iloc[0]+".csv")
            try:
                df.to_csv(output.__str__(),index=False)
            except OSError:
                cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').__str__())
                try:
                    df.to_csv(output.__str__(),index=False)
                except:
                    raise("Não é pra chegar aqui")
        #break

def execFixacao():
    os.chdir(ROOT_APPS)
    lista = list(Path(PATH_RAW_REAL_EYE).parent.joinpath('alunos').glob("*.csv"))
    bar = tqdm(total=len(lista),desc="run_task={}".format('gerando fixações'))
    for i in lista:
        #df = pd.read_csv(i.__str__())
        #input = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
        input = i.__str__()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOFCSV,i.stem+'.csv')
        #print(output)

        cmd = "python3 fixacao_real_eye.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        #print(input)
        #print("fixacao.py"+output2.__str__()+'\n')
        print(os.popen(cmd=cmd).read())
        bar.update(1)
        #break

def makeDirs(lista):
    cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').__str__())
    for i in lista:
        cdCreate(Path(PATH_RAW_REAL_EYE).parent.joinpath('Alunos').joinpath(i).__str__())

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = PATH_TARGET_GROUP.rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    #c=0
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        bg_path = ''
        try:
            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath(input.stem[::-1].split('_',1)[1][::-1]+".png").__str__()+"'"
        except IndexError:
            print('-----\nImagem não encontrada em:',input,'\n------')
        if(input.stem.__str__().find('contagem_e_soma_material_completo') != -1):
            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath("soma_material_completo.png").__str__()+"'"
            cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.parent.joinpath(output.stem.__str__().replace('contagem_e_','')+'.html').__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())

            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath("contagem_material_completo.png").__str__()+"'"
            cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.parent.joinpath(output.stem.__str__().replace('_e_soma','')+'.html').__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())
        else:
            cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())
        #os.popen(cmd=cmd).read()
        bar.update(1)
        '''c+=1
        if(c>=10):
            break'''
        

def execPGraph():
    os.chdir(ROOT_APPS)
    #teste = Path('GazePointHeatMap/Example Output/data.csv')
    csv_finders = PATH_TARGET_HEAT_INPUT.rglob("*.csv")
    csv_finders = list(csv_finders)
    #csv_finders = list([teste])
    #c=0
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        #output = Path('GazePointHeatMap/Example Output/teste.html')
        output = Path.joinpath(i.parent.parent.absolute(),'point_graph',i.stem+'.html')
        bg_path = ''
        try:
            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath(input.stem[::-1].split('_',1)[1][::-1]+".png").__str__()+"'"
        except IndexError:
            print('-----\nImagem não encontrada em:',input,'\n------')
        if(input.stem.__str__().find('contagem_e_soma_material_completo') != -1):
            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath("soma_material_completo.png").__str__()+"'"
            cmd = "python3 graficoPontos.py '"+input.__str__()+"' -o '"+output.parent.joinpath(output.stem.__str__().replace('contagem_e_','')+'.html').__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())

            bg_path = " -bg '"+input.parent.parent.joinpath('imgs').joinpath("contagem_material_completo.png").__str__()+"'"
            cmd = "python3 graficoPontos.py '"+input.__str__()+"' -o '"+output.parent.joinpath(output.stem.__str__().replace('_e_soma','')+'.html').__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())
        else:
            cmd = "python3 graficoPontos.py '"+input.__str__()+"' -o '"+output.__str__()+"'"+bg_path+" -tbg '"+i.__str__()[::-1].split('_',1)[0][::-1].split('.')[0]+"'"
            print(os.popen(cmd=cmd).read())
        #os.popen(cmd=cmd).read()
        bar.update(1)
        '''c+=1
        if(c>=10):
            break'''
        #break

def execInputHeatMap():
    os.chdir(ROOT_APPS)
    csv_finders = Path(PATH_TARGET_HEAT_INPUT).rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Gerando csv's para HeatMap"))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),INPUT_CSVTOCSVHEAT,i.stem+'.csv')

        cmd = "python3 toCsv.py '"+input.__str__()+"' -o '"+output.__str__()+"' -hm True"
        #print(cmd)
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...

def execHeatMap():
    os.chdir(ROOT_APPS)
    csv_finders = Path(PATH_RAW_REAL_EYE).parent.joinpath(INPUT_CSVTOCSVHEAT).rglob("*.csv")
    csv_finders = list(csv_finders)
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Gerando graficos de HeatMap"))
    #c=0
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),'heat_graph',i.stem+'.png')
        bg_path = ''
        try:
            bg_path = " -b '"+input.parent.parent.joinpath('imgs').joinpath(input.stem[::-1].split('_',1)[1][::-1]+".png").__str__()+"'"
        except IndexError:
            print('-----\nImagem não encontrada em:',input,'\n------')
        if(input.stem.__str__().find('contagem_e_soma_material_completo') != -1):
            bg_path = " -b '"+input.parent.parent.joinpath('imgs').joinpath("soma_material_completo.png").__str__()+"'"
            cmd = "python3 gazeheatplot.py '"+input.__str__()+"' "+str(SCREEN_W)+" "+str(SCREEN_H)+" -a 0.6 -o '"+output.parent.joinpath(output.stem.__str__().replace('contagem_e_','')+'.png').__str__()+"'"+bg_path
            print(os.popen(cmd=cmd).read())

            bg_path = " -b '"+input.parent.parent.joinpath('imgs').joinpath("contagem_material_completo.png").__str__()+"'"
            cmd = "python3 gazeheatplot.py '"+input.__str__()+"' "+str(SCREEN_W)+" "+str(SCREEN_H)+" -a 0.6 -o '"+output.parent.joinpath(output.stem.__str__().replace('_e_soma','')+'.png').__str__()+"'"+bg_path
            print(os.popen(cmd=cmd).read())
        else:
            cmd = "python3 gazeheatplot.py '"+input.__str__()+"' "+str(SCREEN_W)+" "+str(SCREEN_H)+" -a 0.6 -o '"+output.__str__()+"'"+bg_path
            print(os.popen(cmd=cmd).read())
        bar.update(1)
        '''c+=1
        if(c>=10):
            break'''
        
    ...

#separateByTarget()
#execFixacao()
execFGraph()
execPGraph()
#execInputHeatMap()
execHeatMap()