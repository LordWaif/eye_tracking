DEFAULT_SEP = ','
DEFAULT_ENCODING = 'utf-8'
DEFAULT_NAN = 'NaN'

DEFAULT_DATE_SEP,DEFAULT_DATE_RPL = '_','/'
DEFAULT_TIME_SEP,DEFAULT_TIME_RPL = '_',':'
DEFAULT_MILL_SEP,DEFAULT_MILL_RPL = '.',':'

DEFAULT_EXCLUDE_CONDITIONS = [(0,'==',0)]
DEFAULT_HAS_DATE = True

#(saida,str(1),csv) -> 'saida'+'1'+'.'+'csv' -> saida1.csv
path_design = lambda path_design: path_design[0]+path_design[1]+'.'+path_design[2]

COLUMNS_NAMES_DATAFRAME = ['CLASSE','INDICE','DATE_TIME','X_TELA','Y_TELA','X_MOUSE','Y_MOUSE','V1','V2','V3','V4','V5','V6','V7','NOME']