import argparse,os
import pandas as pd

parser = argparse.ArgumentParser(description="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo txt')

#opcional
parser.add_argument('-o','--output-name', default='output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-m','--many', type=bool, default=False,required=False, help='conversao para varios txt do caminho')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']

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
            except Exception as e:
                if(str(e).find('invalid literal for int()') == 0):
                    ret.append(True)
                
    return all(ret)

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
    arquivo = [arquivo[i].split(sep) for i in range(len(arquivo))]
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
    i=0
    while i<len(excluidos):
        arquivo.remove(excluidos[i])    
        i+=1
    if len(arquivo) != 0:
        df = pd.DataFrame(arquivo)
        df.columns = COLUMNS_NAMES_DATAFRAME
        df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format="%Y"+date_rpl+"%m"+date_rpl+"%d %H"+time_rpl+"%M"+time_rpl+"%S"+mill_rpl+"%f")
        df.to_csv(path_out,sep=sep_dataframe,encoding=encoding,index=False)

if not(args['many']):
    txt2csv()
else:
    c = 0
    for i in os.listdir(PATH_IN):
        c += 1
        p,ex = os.path.splitext(OUTPUT_NAME)
        txt2csv(path_in=os.path.join(PATH_IN,i),path_out=path_design([p,str(c),ex]))


#COMMAND python3 toCsv.py ./input -o ./output/saida.csv -m true
#COMMAND python3 toCsv.py ./in -o ./out/saida.csv -m true
