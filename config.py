#ROOT_DATA = '/home/lordwaif/documents/dados_eyeTree'
ROOT_DATA = '/home/lordwaif/documents/eye_leoTree'

ROOT_APPS = '/home/lordwaif/documents/eye_tracking'
IMAGE_ROOT = '/home/lordwaif/documents/dados_eyeTree/bg.jpeg'
#IMAGE_PATH = '/home/lordwaif/documents/dados_eyeTree/imgs'
IMAGE_PATH = '/home/lordwaif/documents/eye_leoTree/imgs'
VIRTUAL_ENVIROMENT = '/home/lordwaif/documents/venv'
PATH_N_FIX_TABLE = '/home/lordwaif/documents/dados_eyeTree'

COLUMNS_FIXACION_REGIONS = ['MS','X','Y','DURACAO_FRAMES','DATE_FIM']
OUTLIER = 1000

#IMAGE_NAME_PREFFIX = 'Slide'
IMAGE_NAME_PREFFIX = 'Video_'
#IMAGE_NAME_SUFFIX = '.PNG'
IMAGE_NAME_SUFFIX = '.png'

TEMPORAY_COMPACT_FOLDER = '/home/lordwaif/documents/temp_compact'

GRAPH_TITLE_DEFAULT = 'Teste'

DEFAULT_SEP = ','
DEFAULT_SEP_DF = DEFAULT_SEP
DEFAULT_ENCODING = 'utf-8'
DEFAULT_NAN = 'NaN'

DEFAULT_PATH_GRAPHS_FIX = '/home/lordwaif/documents/dados_eyeTree/imgs/test.html'

DEFAULT_DATE_SEP,DEFAULT_DATE_RPL = '_','/'
DEFAULT_TIME_SEP,DEFAULT_TIME_RPL = '_',':'
DEFAULT_MILL_SEP,DEFAULT_MILL_RPL = '.',':'

DEFAULT_EXCLUDE_CONDITIONS = [(2,'==',''),(-1,'==','teste')]
DEFAULT_HAS_DATE = True

DEFAULT_COLUMNS_TO_BE_DROPPED = ['V1','V2','V3','V4','V5','V6','V7']
COLUMNS_TO_BE_PROCESS = {'X':'X_TELA','Y':'Y_TELA','N':'TELA','C':'CLASSE'}

SCREEN_W = 1280
SCREEN_H = 720
TIME_MILLIS_REGION = 100
RANGE_X = 50
RANGE_Y = RANGE_X
'''
RANGE_X = int(SCREEN_W*0.03)
RANGE_Y = int(SCREEN_H*0.06)
'''

#(saida,str(1),csv) -> 'saida'+'1'+'csv' -> saida1.csv
path_design = lambda path_design: path_design[0]+path_design[2]

COLUMN_DATE_TIME = 'DATE_TIME'
COLUMNS_NAMES_DATAFRAME = ['CLASSE','INDICE',COLUMN_DATE_TIME,'X_TELA','Y_TELA','X_MOUSE','Y_MOUSE','V1','V2','V3','V4','V5','V6','V7','NOME']

REGIONS = {
    "adicao_robo":[
        {'relevante':
            [[(43,708),(1081,492)]]
        },],
    "adicao_baixa_acessibilidade":[
        {'relevante':
            [[(60,663),(282,235)],[(435,433),(859,295)]]
        },],
    "soma_2":[
        {'relevante':
            [[(58,618),(1233,588)],[(333,200),(744,58)]]
        },],
    "contagem_material_completo":[
        {'relevante':
            [[(109,656),(1158,171)]]
        },],
    "contagem_passaro":[
        {'relevante':
            [[(73,595),(889,543)],[(547,309),(887,190)]]
        },],
    "soma_material_completo":[
        {'relevante':
            [[(113,645),(1139,153)]]
        },],
}