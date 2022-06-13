#%%
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.graph_objects as px 
import numpy as np
from PIL import Image
from datetime import datetime as dt

from GazePointHeatMap.heatmap import segmentar

PATH = "video_1_multiplicacao"
df = pd.read_csv(PATH+'.csv',sep=';')
df = df.drop(columns=['Unnamed: 0','V1','V2','V3'])

def regionFinder(x,y,r):
    regiao = []
    count_regiao = 1
    x_anterior = x[0]-r
    x_fim = x[0] + r

    y_anterior = y[0]-r
    y_fim = y[0] + r

    regiao = []
    count_regiao = 1
    lista_x_medio,lista_y_medio = [],[]
    coordenadas_tela = np.transpose(np.asarray([x,y]))
    for i,j in coordenadas_tela:
        x_regiao = (i >= x_anterior and i<x_fim)
        y_regiao = (j >= y_anterior and j<y_fim)
        lista_x_medio.append((x_anterior+x_fim)/2)
        lista_y_medio.append((y_anterior+y_fim)/2)
        if not(x_regiao and y_regiao):
            x_anterior,x_fim = i-r,i+r
            y_anterior,y_fim = j-r,j+r
            count_regiao+=1
        regiao.append(count_regiao)
    return [regiao,lista_x_medio,lista_y_medio]


def gerarFixacao(df,tipo='tela',r=25,t=100,w = 1280,h = 720,titulo='grafico',image_bg='frame_video1.png'):
    tipo = tipo.upper()
    x = df['X_'+tipo].values
    y = df['Y_'+tipo].values
    df['REGIAO_'+tipo],df['X_REGIAO_MEDIO_'+tipo],df['Y_REGIAO_MEDIO_'+tipo] = regionFinder(x,y,r)
    grp = df.groupby('REGIAO_'+tipo)
    df.to_csv('verificacao.csv',sep=';')
    x_medio = grp['X_REGIAO_MEDIO_'+tipo].mean()
    y_medio = grp['Y_REGIAO_MEDIO_'+tipo].mean()
    t_inicio = grp['DATE_TIME'].min().tolist()
    t_fim = grp['DATE_TIME'].max().tolist()

    t_inicio = np.array([dt.strptime(i,'%Y-%m-%d %H:%M:%S.%f') for i in t_inicio])
    t_fim = np.array([dt.strptime(i,'%Y-%m-%d %H:%M:%S.%f') for i in t_fim])
    duracao = t_fim - t_inicio
    duracao = np.array([i.total_seconds()*1000 for i in duracao])
    print(type(duracao[0]))
    reg_count = pd.DataFrame([duracao,x_medio,y_medio,grp.count()['CLASSE']]).T
    reg_count.columns = ['MS','X','Y','DURACAO_FRAMES']
    reg_count = reg_count[reg_count['MS']>t]
    reg_count = reg_count[reg_count['X']<w]
    reg_count = reg_count[reg_count['X']>0]
    reg_count = reg_count[reg_count['Y']>0]
    reg_count = reg_count[reg_count['Y']<h]
    from GazePointHeatMap import heatmap,variaveis as var
    if(var.segmentar):
        l = heatmap.segmentar(reg_count)
        with open ('GazePointHeatMap/n_fixacoes.txt','w') as file:
            for i in l :
                file.write(str(len(i))+'\n')
            file.close()
    else:
        l = [reg_count]
        with open ('GazePointHeatMap/n_fixacoes.txt','w') as file:
            file.write(str(len(reg_count)))
            file.close()
    if(reg_count['MS'].empty):
        tam_maximo = 100
    else:
        tam_maximo = max(reg_count['MS'])
    
    image = Image.open(image_bg)
    plot = px.Figure(
        data=[px.Scatter(
            x=reg_count['X'],
            y=reg_count['Y'],
            mode='markers',
            marker=dict(
                size=reg_count['MS'],
                sizemode='area', 
                sizeref=2.*tam_maximo/(50.**2), 
                sizemin=4,
            ),
        )],
        layout=px.Layout(
            images=[
                dict(
                visible=True,
                source=image,
                xref="x",
                yref="y",
                x=0,
                y=3,
                sizex=1280,
                sizey=720,
                sizing="stretch",
                opacity=0.5,
                layer="below")
            ]
        )
    )

    plot.update_xaxes(showgrid=False,range=[0,1280])
    plot.update_yaxes(showgrid=False,range=[720,0])
    plot.update_layout(title=titulo)

    plot.update_layout(template="plotly_white")
    #plot.update_yaxes(autorange="reversed")
    plot.write_html(titulo+'.html')
    plot.show()

gerarFixacao(df,tipo='tela')

# %%
