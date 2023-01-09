#%%
import pandas as pd
from config import *
import numpy as np
from datetime import datetime as dt
import argparse,os

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo csv')

#opcional
parser.add_argument('-o','--output-name', default='region_output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-m','--many', type=bool, default=False,required=False, help='processamento de varios csv"s')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']

def setAxis(x,y,range_x,range_y):
    x_anterior = x-range_x
    x_fim = x + range_x
    y_anterior = y-range_y
    y_fim = y + range_y
    return [x_anterior,x_fim,y_anterior,y_fim]

class Fixacao():
    def __init__(self,PATH) -> None:
        self.PATH = PATH
        dataframe = pd.read_csv(PATH,sep=DEFAULT_SEP_DF,encoding=DEFAULT_ENCODING)

        self.dataframe = dataframe
        self.regions = None
    
    def rangeCalc(self,look,ind,x,y,range_x=RANGE_X,range_y=RANGE_Y):
        regiao = []
        count_regiao = 1

        x_anterior,x_fim,y_anterior,y_fim = setAxis(x[0],y[0],range_x,range_y)
        lista_x_medio,lista_y_medio = [],[]

        coordenadas_tela = np.transpose(np.asarray([x,y]))
        dead_area = False
        counter_look = 0
        for i,j in coordenadas_tela:
            if(look[counter_look] == 1):
                dead_area = False
            if dead_area:
                x_anterior,x_fim,y_anterior,y_fim = setAxis(i,j,range_x,range_y)

                lista_x_medio.append((x_anterior+x_fim)/2)
                lista_y_medio.append((y_anterior+y_fim)/2)
                regiao.append(-1)
                #print([ind[counter_look],regiao[-1],lista_x_medio[-1],lista_y_medio[-1]])
                counter_look += 1
                continue
            x_regiao = (i >= x_anterior and i<x_fim)
            y_regiao = (j >= y_anterior and j<y_fim)
            if not(x_regiao and y_regiao) or (look[counter_look] == 0):
                dead_area = True
                x_anterior,x_fim,y_anterior,y_fim = setAxis(i,j,range_x,range_y)
                count_regiao+=1
            lista_x_medio.append((x_anterior+x_fim)/2)
            lista_y_medio.append((y_anterior+y_fim)/2)
            if look[counter_look] == 0:
                regiao.append(-1)
            else:
                regiao.append(count_regiao)
            #print([ind[counter_look],regiao[-1],lista_x_medio[-1],lista_y_medio[-1]])
            counter_look += 1
        #print(len(regiao),len(lista_x_medio),len(lista_y_medio))
        return [regiao,lista_x_medio,lista_y_medio]

    def regionFinder(self,columns_tobe_process=COLUMNS_TO_BE_PROCESS):
        axisX = self.dataframe[columns_tobe_process['X']].values
        axisY = self.dataframe[columns_tobe_process['Y']].values
        look = self.dataframe[columns_tobe_process['C']].values
        ## Calculando regiões
        self.dataframe['REGIAO_'+COLUMNS_TO_BE_PROCESS['N']],self.dataframe['X_REGIAO_MEDIO_'+COLUMNS_TO_BE_PROCESS['N']],self.dataframe['Y_REGIAO_MEDIO_'+COLUMNS_TO_BE_PROCESS['N']] = self.rangeCalc(look,np.asarray(self.dataframe.index),axisX,axisY)
        #self.dataframe.to_csv(self.PATH,sep=DEFAULT_SEP_DF,encoding=DEFAULT_ENCODING,index=False)
        ##Processando Regiões
        return self.regionProcess()

    def getRegions(self):
        if self.regions == None:
            self.regions = self.regionFinder()
        return self.regions
    
    def saveRegions(self,dataframe,
                    path_out,
                    sep_dataframe=DEFAULT_SEP_DF,
                    encoding=DEFAULT_ENCODING):
        dataframe.to_csv(path_out,sep=sep_dataframe,encoding=encoding,index=False)

    def group(self,colum_tobe_grouped='REGIAO_'+COLUMNS_TO_BE_PROCESS['N']):
        return self.dataframe[self.dataframe[colum_tobe_grouped] != -1].groupby(colum_tobe_grouped)

    def timeProcess(self,grp):
        #print(grp[''])
        #print(grp['MS'].sum())
        '''
        t_inicio = grp['MS'].min().tolist()
        t_fim = grp[COLUMN_DATE_TIME].max().tolist()
        t_inicio = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_inicio])
        t_fim = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_fim])
        duracao = t_fim - t_inicio
        duracao = np.array([i.total_seconds()*1000 for i in duracao])

        tempo_inicio_geral = dt.strptime(grp[COLUMN_DATE_TIME].min().iloc[0],r'%Y-%m-%d %H:%M:%S.%f')
        tempo_final_geral = dt.strptime(grp[COLUMN_DATE_TIME].max().iloc[-1],r'%Y-%m-%d %H:%M:%S.%f')
        return [duracao,tempo_inicio_geral,tempo_final_geral]'''
        return [grp['MS'].sum()]
    
    def regionProcess(self,columns_sufix=COLUMNS_TO_BE_PROCESS['N']):
        grp = self.group()
        duracoes = self.timeProcess(grp)[0]
        '''for i in grp:
            if i[1]['MS'].sum() > 10000:
                ...
                print(i[1]['MS'])'''

        x_medio = grp['X_REGIAO_MEDIO_'+columns_sufix].mean()
        y_medio = grp['Y_REGIAO_MEDIO_'+columns_sufix].mean()
        #print(grp.count()['CLASSE'])
        region_counter = pd.DataFrame([duracoes,x_medio,y_medio,grp.count()['CLASSE'],grp['MS'].max()]).T
        col = COLUMNS_FIXACION_REGIONS
        region_counter.columns = col
        region_counter = region_counter[region_counter[col[0]]>TIME_MILLIS_REGION]
        region_counter = region_counter[region_counter[col[1]]<SCREEN_W]
        region_counter = region_counter[region_counter[col[1]]>0]
        region_counter = region_counter[region_counter[col[2]]>0]
        region_counter = region_counter[region_counter[col[2]]<SCREEN_H]
        return region_counter

if not(args['many']):
    f = Fixacao(PATH_IN)
    regioes = f.getRegions()
    p,ex = os.path.splitext(OUTPUT_NAME)
    c = 0
    f.saveRegions(regioes,path_out=path_design([p,str(c),ex]))
else:
    c = 0
    for i in os.listdir(PATH_IN):
        c += 1
        p,ex = os.path.splitext(OUTPUT_NAME)
        f = Fixacao(os.path.join(PATH_IN,i))
        regioes = f.getRegions()
        f.saveRegions(regioes,path_out=path_design([p,ex]))
        #txt2csv(path_in=os.path.join(PATH_IN,i),path_out=path_design([p,str(c),ex]))

#COMMAND python3 fixacao.py ./output -o ./output_regions/regioes.csv -m true
#COMMAND python3 fixacao.py ./out -o ./out_regions/regioes.csv -m true