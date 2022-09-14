# -*- coding: utf-8 -*-
from ntpath import join
import os
from paraCsv import transformCsv
from GazePointHeatMap.heatmap import segmentar
from GazePointHeatMap.gazeheatplot import gerarGazeHeatMap
#Porque eu comentei?
from fixacao import gerarTodaFixacoes
import re,pandas as pd
PATH_DADOS = '/home/lordwaif/documents/eye_tracking/Dados brutos'
PATH_BG = '/home/lordwaif/documents/eye_tracking/GazePointHeatMap/img_bg'
pessoas_testes = [dir for dir in os.listdir(PATH_DADOS) if os.path.isdir(os.path.join(PATH_DADOS, dir))]

def gerarCsv():
    for i in pessoas_testes:
        path = os.path.join(PATH_DADOS,i)
        arquivos = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and os.path.splitext(file)[1] == '.txt']
        for j in arquivos:
            path_dado_pessoa = os.path.join(path,j)
            transformCsv(path_dado_pessoa)
            #print(os.path.dirname(path_dado_pessoa))

import re 
exp1  = re.compile(r'(v[íi]deo[ ]{0,2})([0-9])',re.IGNORECASE)     
exp2  = re.compile(r'frame_video([0-9])$',re.IGNORECASE) 
exp3 = re.compile(r'heat_map',re.IGNORECASE) 
exp4  = re.compile(r'(deo[ ]{0,2})([0-9])',re.IGNORECASE)  
exp5  = re.compile(r'heat_map([0-9])_([0-9])',re.IGNORECASE)  
exp6  = re.compile(r'frame_video([0-9])_resized$',re.IGNORECASE) 
def gerarGraficos():
    bgs = getBg()
    for i in pessoas_testes:
        path = os.path.join(PATH_DADOS,i)
        arquivos = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and os.path.splitext(file)[1] == '.csv']
        for j in arquivos:
            path_dado_pessoa = os.path.join(path,j)
            if  not re.search(exp3,os.path.splitext(path_dado_pessoa.split('/')[-1])[0]):
                n_video = re.search(exp1,path_dado_pessoa.split('/')[-1]).group(2)
                gerarTodaFixacoes(path_dado_pessoa,bgs[n_video])
                #print(path_dado_pessoa)
def getBg():
    bgs = dict()
    for bg in os.listdir(PATH_BG):
        pesq = re.search(exp2,os.path.splitext(bg)[0])
        if pesq:
            bgs[pesq.group(1)] = os.path.join(PATH_BG,bg)
    return bgs
def getBgr():
    bgs = dict()
    for bg in os.listdir(PATH_BG):
        pesq = re.search(exp6,os.path.splitext(bg)[0])
        if pesq:
            bgs[pesq.group(1)] = os.path.join(PATH_BG,bg)
    return bgs
#gerarGraficos()

def gerarDadosHeatMap():
    for i in pessoas_testes:
        path = os.path.join(PATH_DADOS,i)
        arquivos = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and os.path.splitext(file)[1] == '.csv']
        for j in arquivos:
            path_dado_pessoa = os.path.join(path,j)
            if  not re.search(exp3,os.path.splitext(path_dado_pessoa.split('/')[-1])[0]):
                df = pd.read_csv(path_dado_pessoa,sep=';',encoding='utf-8')
                df_aux = pd.DataFrame([df['X_TELA'],df['Y_TELA']]).T
                df_aux.columns = ['X','Y']
                df_aux = df_aux.astype(int)
                nome = os.path.splitext(path_dado_pessoa.split('/')[-1])[0]+'_heat_map'
                PATH = os.path.dirname(path_dado_pessoa)
                #print(os.path.join(PATH,nome))
                segmentar(df_aux,PATH,nome)
#gerarDadosHeatMap()

def gerarHeatMap():
    bgs = getBgr()
    for i in pessoas_testes:
        path = os.path.join(PATH_DADOS,i)
        arquivos = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path,file)) and os.path.splitext(file)[1] == '.csv']
        for j in arquivos:
            path_dado_pessoa = os.path.join(path,j)
            #print(path_dado_pessoa)
            if re.search(exp3,os.path.splitext(path_dado_pessoa.split('/')[-1])[0]):
                print(path_dado_pessoa)
                n_video = re.search(exp4,os.path.splitext(path_dado_pessoa.split('/')[-1])[0]).group(2)
                display_width = 1280
                display_height = 720
                alpha = 0.6
                ngaussian = 200
                sd = 33.0
                x = re.search(exp5,path_dado_pessoa.split('/')[-1]).group(1)
                y = re.search(exp5,path_dado_pessoa.split('/')[-1]).group(2)
                saida = path_dado_pessoa.split('.')[0]+'_heat_map_'+str(x)+'_'+str(y)+'.png'
                gerarGazeHeatMap(path_dado_pessoa,1280,720,alpha,saida,bgs[n_video],ngaussian,sd,int(x))


gerarHeatMap()

