#%%
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.graph_objects as px 
import numpy as np
from PIL import Image
from datetime import datetime as dt, timedelta
import os

from GazePointHeatMap.heatmap import segmentar
if __name__ == '__name__':
    PATH = "video_1_multiplicacao"
def gerarTodaFixacoes(PATH,img_bg):
    df = pd.read_csv(PATH,sep=';')
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


    def gerarFixacao(df,tipo='tela',r=25,t=100,w = 1280,h = 720,titulo='',image_bg=img_bg):
        tipo = tipo.upper()
        x = df['X_'+tipo].values
        y = df['Y_'+tipo].values
        df['REGIAO_'+tipo],df['X_REGIAO_MEDIO_'+tipo],df['Y_REGIAO_MEDIO_'+tipo] = regionFinder(x,y,r)
        grp = df.groupby('REGIAO_'+tipo)
        #df.to_csv(os.path.join(os.path.dirname(PATH),'verificacao.csv'),sep=';')
        x_medio = grp['X_REGIAO_MEDIO_'+tipo].mean()
        y_medio = grp['Y_REGIAO_MEDIO_'+tipo].mean()
        t_inicio = grp['DATE_TIME'].min().tolist()
        t_fim = grp['DATE_TIME'].max().tolist()

        t_inicio = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_inicio])
        t_fim = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in t_fim])
        duracao = t_fim - t_inicio
        duracao = np.array([i.total_seconds()*1000 for i in duracao])
        reg_count = pd.DataFrame([duracao,x_medio,y_medio,grp.count()['CLASSE'],grp['DATE_TIME'].max()]).T
        reg_count.columns = ['MS','X','Y','DURACAO_FRAMES','DATE_FIM']
        reg_count = reg_count[reg_count['MS']>t]
        reg_count = reg_count[reg_count['X']<w]
        reg_count = reg_count[reg_count['X']>0]
        reg_count = reg_count[reg_count['Y']>0]
        reg_count = reg_count[reg_count['Y']<h]
        from GazePointHeatMap import heatmap,variaveis as var
        tempo_inicio_geral = dt.strptime(df['DATE_TIME'].min(),r'%Y-%m-%d %H:%M:%S.%f')
        tempo_video = np.array([dt.strptime(i,r'%Y-%m-%d %H:%M:%S.%f') for i in reg_count['DATE_FIM'].tolist()])-tempo_inicio_geral
        #str((timedelta(seconds=i.total_seconds()).seconds)//60)+':'+str((timedelta(seconds=i.total_seconds()).seconds)%60)
        #str(timedelta(seconds=i.total_seconds()))

        tempo_video = [str(timedelta(seconds=i.total_seconds())).split('.')[0] for i in tempo_video]
        reg_count['DATE_FIM'] = tempo_video
        reg_count = reg_count.sort_values('DATE_FIM')
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
        #tempo_fim_geral = dt.strptime(df['DATE_TIME'].max(),r'%Y-%m-%d %H:%M:%S.%f')
        #duracao_video = (tempo_fim_geral-tempo_inicio_geral).total_seconds()
        #print(reg_count)
        def grafico_linha(list_df):
            for i,ldf in enumerate(list_df):
                #print(ldf['MS'])
                plot = px.Figure(
                    data=[px.Line(
                        x=ldf['DATE_FIM'],
                        y=ldf['MS'].cumsum(axis = 0)/1000,
                    )],
                )
                #plot.update_xaxes(showgrid=False,range=[0,1280])
                #plot.update_yaxes(showgrid=False,range=[0,720])
                plot.update_layout(title=titulo+' de linha regiao'+str(i+1))
                plot.update_layout(template="plotly_white")
                #plot.update_yaxes(autorange="reversed")
                plot.write_html(os.path.join(os.path.dirname(PATH),os.path.splitext(PATH)[0].split('/')[-1]+titulo+'_Fixacao Acumulada_'+df['NOME'][0]+'_'+str(i)+'_.html'))
                #plot.show()
        def graficos_fixacao(list_df):
            image = Image.open(image_bg)
            for i,ldf in enumerate(list_df):
                plot = px.Figure(
                    data=[px.Scatter(
                        x=ldf['X'],
                        y=ldf['Y'],
                        mode='markers',
                        marker=dict(
                            size=ldf['MS'].astype('float32'),
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
                plot.update_layout(title=titulo+' Nome: '+df['NOME'][0]+' N Fixacoes: '+str(len(ldf)))

                plot.update_layout(template="plotly_white")
                #plot.update_yaxes(autorange="reversed")
                plot.write_html(os.path.join(os.path.dirname(PATH),os.path.splitext(PATH)[0].split('/')[-1]+titulo+'_'+df['NOME'][0]+'_'+str(i)+'_.html'))
                #plot.show()
        graficos_fixacao(l)
        grafico_linha(l)

    gerarFixacao(df,tipo='tela')

# %%
