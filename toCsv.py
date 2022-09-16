import argparse,os
import pandas as pd

parser = argparse.ArgumentParser(descricao="Parametro para execução")

#obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo txt')

#opcional
parser.add_argument('-o','--output-name', default='output.csv', type=str, required=False, help='nome do arquivo de saida')
parser.add_argument('-m','--many', type=bool, required=False, help='conversao para varios txt do caminho')

args = vars(parser.parse_args())

PATH_IN = args['input-path']
OUTPUT_NAME = args['output_name']

DEFAULT_SEP = ','
DEFAULT_ENCODING = 'utf-8'
DEFAULT_NAN = 'NaN'

DEFAULT_DATE_SEP,DEFAULT_DATE_RPL = '_','/'
DEFAULT_TIME_SEP,DEFAULT_TIME_RPL = '_',':'
DEFAULT_MILL_SEP,DEFAULT_MILL_RPL = '.',':'

DEFAULT_EXCLUDE_CONDITIONS = [(0,'==',0)]
DEFAULT_HAS_DATE = True

dds,dts,dms = DEFAULT_DATE_SEP,DEFAULT_TIME_SEP,DEFAULT_MILL_SEP

INCOMING_FORMAT_DATE = "YYYY{}m{}d H{}M{}S{}F".format(dds,dds,dts,dts,dms)
COUNT_FORMAT_DATE = (2,2,1)

def exclude_conditions(elemento,args):
    ret = []
    for i in args:
        ret.append(eval("elemento[i[0]] i[2] i[1]"))
    return all(ret)

def txt2csv(path_in=PATH_IN,
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
            _exclude_conditions=DEFAULT_EXCLUDE_CONDITIONS):
    cfd = count_format_date

    arquivo = []
    with open(PATH_IN,'r',encoding=encoding) as file:
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

    df = pd.DataFrame(arquivo)
    df.columns = ['CLASSE','INDICE','DATE_TIME','X_TELA','Y_TELA','X_MOUSE','Y_MOUSE','V1','V2','V3','V4','V5','V6','V7','NOME']
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format="%Y/%m/%d %H:%M:%S:%f")
    df.to_csv(os.path.splitext(path_in)[0]+OUTPUT_NAME,sep=';',encoding=encoding)
    