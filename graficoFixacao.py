import plotly.graph_objects as px 
import os
from config import *
'''
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
'''


class GraficoFixacao():
    def __init__(self,region_counter) -> None:
        self.region_counter = region_counter

    def makeGraph(self,path=DEFAULT_PATH_GRAPHS_FIX):
        tam_maximo = max(self.region_counter['MS'])
        plot = px.Figure(
                    data=[px.Scatter(
                        x=self.region_counter['X'],
                        y=self.region_counter['Y'],
                        mode='markers',
                        marker=dict(
                            size=self.region_counter['MS'].astype('float32'),
                            sizemode='area', 
                            sizeref=2.*tam_maximo/(50.**2), 
                            sizemin=4,
                        ),
                    )],
                )
        plot.update_xaxes(showgrid=False,range=[0,1280])
        plot.update_yaxes(showgrid=False,range=[720,0])
        #titulo+' Nome: '+df['NOME'][0]+' N Fixacoes: '+str(len(ldf))
        plot.update_layout(title='Teste')

        plot.update_layout(template="plotly_white")
        #plot.update_yaxes(autorange="reversed")
        #os.path.join(os.path.dirname(PATH),os.path.splitext(PATH)[0].split('/')[-1]+titulo+'_'+df['NOME'][0]+'_'+str(i)+'_.html')
        plot.write_html(os.path.join(path,'teste.html'))

if __name__ == '__main__':
    import pandas as pd
    GraficoFixacao(pd.read_csv('./output_regions/regioes1.csv',sep=',')).makeGraph()