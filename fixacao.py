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

class Fixacao():
    def __init__(self,PATH) -> None:
        self.PATH = PATH
        dataframe = pd.read_csv(PATH,sep=DEFAULT_SEP_DF,encoding=DEFAULT_ENCODING)
        dataframe = dataframe.drop(columns=DEFAULT_COLUMNS_TO_BE_DROPPED)

        self.dataframe = dataframe
        self.regions = None
    
    def rangeCalc(self,x,y,range_x=RANGE_X,range_y=RANGE_Y):
        regiao = []
        count_regiao = 1
        x_anterior = x[0]-range_x
        x_fim = x[0] + range_x

        y_anterior = y[0]-range_y
        y_fim = y[0] + range_y

        regiao = []
        count_regiao = 1
        lista_x_medio,lista_y_medio = [],[]
        coordenadas_tela = np.transpose(np.asarray([x,y]))
        for i,j in coordenadas_tela:
            x_regiao = (i >= x_anterior and i<x_fim)
            y_regiao = (j >= y_anterior and j<y_fim)
            if not(x_regiao and y_regiao):
                x_anterior,x_fim = i-range_x,i+range_x
                y_anterior,y_fim = j-range_y,j+range_y
                count_regiao+=1
                lista_x_medio.append((x_anterior+x_fim)/2)
                lista_y_medio.append((y_anterior+y_fim)/2)
            else:
                lista_x_medio.append((x_anterior+x_fim)/2)
                lista_y_medio.append((y_anterior+y_fim)/2)
            regiao.append(count_regiao)
        return [regiao,lista_x_medio,lista_y_medio]

    def regionFinder(self,columns_tobe_process=COLUMNS_TO_BE_PROCESS):
        axisX = self.dataframe[columns_tobe_process['X']].values
        axisY = self.dataframe[columns_tobe_process['Y']].values
        ## Calculando regiões
        self.dataframe['REGIAO_'+COLUMNS_TO_BE_PROCESS['N']],self.dataframe['X_REGIAO_MEDIO_'+COLUMNS_TO_BE_PROCESS['N']],self.dataframe['Y_REGIAO_MEDIO_'+COLUMNS_TO_BE_PROCESS['N']] = self.rangeCalc(axisX,axisY)
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
        return self.dataframe.groupby(colum_tobe_grouped)

    def timeProcess(self,grp):
        t_inicio = grp[COLUMN_DATE_TIME].min().tolist()
        t_fim = grp[COLUMN_DATE_TIME].max().tolist()

        t_inicio = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_inicio])
        t_fim = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_fim])
        duracao = t_fim - t_inicio
        duracao = np.array([i.total_seconds()*1000 for i in duracao])

        tempo_inicio_geral = dt.strptime(grp[COLUMN_DATE_TIME].min().iloc[0],r'%Y-%m-%d %H:%M:%S.%f')
        tempo_final_geral = dt.strptime(grp[COLUMN_DATE_TIME].max().iloc[-1],r'%Y-%m-%d %H:%M:%S.%f')
        return [duracao,tempo_inicio_geral,tempo_final_geral]
    
    def regionProcess(self,columns_sufix=COLUMNS_TO_BE_PROCESS['N']):
        grp = self.group()
        duracoes = self.timeProcess(grp)[0]

        x_medio = grp['X_REGIAO_MEDIO_'+columns_sufix].mean()
        y_medio = grp['Y_REGIAO_MEDIO_'+columns_sufix].mean()

        region_counter = pd.DataFrame([duracoes,x_medio,y_medio,grp.count()['CLASSE'],grp['DATE_TIME'].max()]).T
        region_counter.columns = ['MS','X','Y','DURACAO_FRAMES','DATE_FIM']

        region_counter = region_counter[region_counter['MS']>TIME_MILLIS_REGION]
        region_counter = region_counter[region_counter['X']<SCREEN_W]
        region_counter = region_counter[region_counter['X']>0]
        region_counter = region_counter[region_counter['Y']>0]
        region_counter = region_counter[region_counter['Y']<SCREEN_H]
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