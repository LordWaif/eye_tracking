import plotly.graph_objects as px 
import os
import argparse
import pandas as pd
from config import GRAPH_TITLE_DEFAULT,SCREEN_W,SCREEN_H,DEFAULT_SEP_DF

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo csv')

#opcional
parser.add_argument('-o','--output-name', default='region_output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-tbg','--title-bg',default=GRAPH_TITLE_DEFAULT,required=False,help='titulo do grafico gerado')
parser.add_argument('-dots','--dots',default=False,required=False,help='Se o grafico vai ser de linhas ou pontos')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']
BG_TITLE = args['title_bg']
DOTS = args['dots']

def main(path_in=PATH_IN,sep=DEFAULT_SEP_DF):
    df = pd.read_csv(path_in,sep=sep)
    grafico_linha(df,BG_TITLE,OUTPUT_NAME)

def grafico_linha(df,titulo,path=OUTPUT_NAME):
    if not(DOTS):
        plot = px.Figure(
            data=[px.Line(
                x=df['DATE_FIM'],
                y=df['MS'].cumsum(axis = 0)/1000,
            )],
        )
    else:
        plot = px.Figure()
        plot.add_trace(px.Scatter(y=df['MS'].cumsum(axis = 0)/1000, x=df['DATE_FIM'],mode='markers'))
    #plot.update_xaxes(showgrid=False,range=[0,1280])
    #plot.update_yaxes(showgrid=False,range=[0,720])
    plot.update_layout(title=titulo)
    plot.update_layout(template="plotly_white")
    #plot.update_yaxes(autorange="reversed")
    #plot.write_html(path)
    plot.write_image(path[::-1].split('.',1)[1][::-1]+'_dots_acumulada.png',width=SCREEN_W, height=SCREEN_H)
    #plot.show()

main()