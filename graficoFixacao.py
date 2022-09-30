import plotly.graph_objects as px 
import os
from config import *
from PIL import Image
import argparse,os
import pandas as pd

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo csv')

#opcional
parser.add_argument('-o','--output-name', default='region_output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-bg','--bg-image',default=IMAGE_ROOT,type=str,required=False,help='caminho de imagem a ser usada de fundo')
parser.add_argument('-tbg','--title-bg',default=GRAPH_TITLE_DEFAULT,required=False,help='titulo do grafico gerado')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']
BG_IMG = args['bg_image']
BG_TITLE = args['title_bg']


class GraficoFixacao():
    def __init__(self,path_region_counter,image_bg=IMAGE_ROOT,sep=DEFAULT_SEP_DF) -> None:
        self.image_bg = image_bg
        self.region_counter = pd.read_csv(path_region_counter,sep=sep)

    def makeGraph(self,path=OUTPUT_NAME):
        image = Image.open(self.image_bg)
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
        #titulo+' Nome: '+df['NOME'][0]+' N Fixacoes: '+str(len(ldf))
        plot.update_layout(title=BG_TITLE)

        plot.update_layout(template="plotly_white")
        #plot.update_yaxes(autorange="reversed")
        #os.path.join(os.path.dirname(PATH),os.path.splitext(PATH)[0].split('/')[-1]+titulo+'_'+df['NOME'][0]+'_'+str(i)+'_.html')
        plot.write_html(path)

GraficoFixacao(PATH_IN,image_bg=BG_IMG).makeGraph(path=OUTPUT_NAME)