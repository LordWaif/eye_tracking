ROOT_DATA = '/home/lordwaif/documents/dados_eyeTree'

DEFAULT_SEP = ','
DEFAULT_SEP_DF = DEFAULT_SEP
DEFAULT_ENCODING = 'utf-8'
DEFAULT_NAN = 'NaN'

DEFAULT_PATH_GRAPHS_FIX = './output_graficoF'

DEFAULT_DATE_SEP,DEFAULT_DATE_RPL = '_','/'
DEFAULT_TIME_SEP,DEFAULT_TIME_RPL = '_',':'
DEFAULT_MILL_SEP,DEFAULT_MILL_RPL = '.',':'

DEFAULT_EXCLUDE_CONDITIONS = [(0,'==',0),(-1,'==','teste')]
DEFAULT_HAS_DATE = True

DEFAULT_COLUMNS_TO_BE_DROPPED = ['V1','V2','V3','V4','V5','V6','V7']
COLUMNS_TO_BE_PROCESS = {'X':'X_TELA','Y':'Y_TELA','N':'TELA'}

SCREEN_W = 1270
SCREEN_H = 720
TIME_MILLIS_REGION = 100
RANGE_X = 50
RANGE_Y = RANGE_X
'''
RANGE_X = int(SCREEN_W*0.03)
RANGE_Y = int(SCREEN_H*0.06)
'''

#(saida,str(1),csv) -> 'saida'+'1'+'csv' -> saida1.csv
path_design = lambda path_design: path_design[0]+path_design[1]+path_design[2]

COLUMN_DATE_TIME = 'DATE_TIME'
COLUMNS_NAMES_DATAFRAME = ['CLASSE','INDICE',COLUMN_DATE_TIME,'X_TELA','Y_TELA','X_MOUSE','Y_MOUSE','V1','V2','V3','V4','V5','V6','V7','NOME']