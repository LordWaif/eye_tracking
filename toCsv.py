import argparse,os
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo txt')

#opcional
parser.add_argument('-o','--output-name', default='output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-m','--many', type=bool, default=False,required=False, help='conversao para varios txt do caminho')
parser.add_argument('-hm','--heat-map',type=bool,default=False,required=False)

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']
IS_TO_HEATMAP = args['heat_map']

#print(PATH_IN)

from config import *

dds,dts,dms = DEFAULT_DATE_SEP,DEFAULT_TIME_SEP,DEFAULT_MILL_SEP

INCOMING_FORMAT_DATE = "YYYY{}m{}d H{}M{}S{}F".format(dds,dds,dts,dts,dms)
COUNT_FORMAT_DATE = (2,2,1)

def exclude_conditions(elemento,args):
    ret = []
    for i in args:
        if i[1] == '==':
            try:
                ret.append(int(elemento[i[0]]) == i[2])
            except:
                pass
            try:
                ret.append(elemento[i[0]] == i[2])
            except:
                pass  
            try:
                ret.append(elemento[3][0] == '-2147483648')
            except:
                pass       
    return any(ret)

def txt2csv(path_in=PATH_IN,
            path_out=OUTPUT_NAME,
            sep=DEFAULT_SEP,
            encoding=DEFAULT_ENCODING,
            date_sep=DEFAULT_DATE_SEP,
            time_sep=DEFAULT_TIME_SEP,
            mill_sep=DEFAULT_MILL_SEP,
            date_rpl=DEFAULT_DATE_RPL,
            time_rpl=DEFAULT_TIME_RPL,
            mill_rpl=DEFAULT_MILL_RPL,
            nan=DEFAULT_NAN,
            has_date=DEFAULT_HAS_DATE,
            count_format_date=COUNT_FORMAT_DATE,
            _exclude_conditions=DEFAULT_EXCLUDE_CONDITIONS,
            sep_dataframe=DEFAULT_SEP_DF):
    cfd = count_format_date

    arquivo = []
    with open(path_in,'r',encoding=encoding) as file:
        arquivo = file.readlines()
        file.close()
    import re
    atividades = []
    mark = -1
    for i,elem in enumerate(arquivo):
        if re.match(re.compile('#####,.#####'),elem):
            atividades.append(arquivo[mark+1:i])
            mark = i
    atv = 0
    for j in atividades:
        arquivo = [j[i].split(sep) for i in range(len(j))]
        excluidos = []
        for i in range(len(arquivo)):
            if(exclude_conditions(arquivo[i],_exclude_conditions)):
                excluidos.append(arquivo[i])
                continue
            for j in range(len(arquivo[i])):
                arquivo[i][j] = arquivo[i][j].replace('(','')
                arquivo[i][j] = arquivo[i][j].replace(')','')
                arquivo[i][j] = arquivo[i][j].replace('\n','')
                if has_date:
                    arquivo[i][j] = arquivo[i][j].replace(date_sep,date_rpl,cfd[0])
                    arquivo[i][j] = arquivo[i][j].replace(time_sep,time_rpl,cfd[1])
                    arquivo[i][j] = arquivo[i][j].replace(mill_sep,mill_rpl,cfd[2])
                else:
                    arquivo[i][j] = arquivo[i][j].replace(' ','')
                if(arquivo[i][j] == nan): arquivo[i][j] = None
                try:
                    arquivo[i][j] = float(arquivo[i][j])
                except:
                    pass
        if(len(excluidos)==len(arquivo)):
            continue
        i=0
        while i<len(excluidos):
            arquivo.remove(excluidos[i])    
            i+=1
        # A ultima linha estava vindo vazia, dá pra usar isso ou dropna()
        if(str(arquivo[-1]) == "['']"):
            arquivo = arquivo[:-1]
        if len(arquivo) != 0:
            df = pd.DataFrame(arquivo)
            df.columns = COLUMNS_NAMES_DATAFRAME
            df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format="%Y"+date_rpl+"%m"+date_rpl+"%d %H"+time_rpl+"%M"+time_rpl+"%S"+mill_rpl+"%f")
            output = Path(path_out)
            df.to_csv(os.path.join(output.parent,output.stem+'_atv_'+str(atv)+'_'+output.suffix),sep=sep_dataframe,encoding=encoding,index=False)
            atv += 1

def adapterInputHeatMap(path_in=PATH_IN,
            path_out=OUTPUT_NAME,
            encoding=DEFAULT_ENCODING,
            sep_dataframe=DEFAULT_SEP_DF):
    dataframe_input = pd.read_csv(path_in,sep=sep_dataframe,encoding=encoding)
    df_aux = pd.DataFrame([dataframe_input['X_TELA'],dataframe_input['Y_TELA']]).T
    df_aux.columns = ['X','Y']
    df_aux = df_aux.astype(int)
    df_aux.to_csv(path_out,sep=sep_dataframe,index=False,encoding=encoding)
    ...

if not(IS_TO_HEATMAP):
    if not(args['many']):
        txt2csv()
    else:
        c = 0
        for i in os.listdir(PATH_IN):
            c += 1
            p,ex = os.path.splitext(OUTPUT_NAME)
            txt2csv(path_in=os.path.join(PATH_IN,i),path_out=path_design([p,ex]))
else:
    adapterInputHeatMap()


#COMMAND python3 toCsv.py ./input -o ./output/saida.csv -m true
#COMMAND python3 toCsv.py ./in -o ./out/saida.csv -m true
