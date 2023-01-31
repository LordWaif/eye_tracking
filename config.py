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
    1:[[(0,135),(1323,0)],
        [(0,295),(1323,135)],
        [(0,523),(1323,295)],
        [(0,590),(1323,524)],
        [(0,650),(366,590)],
        [(366,650),(1323,590)],
        [(0,756),(366,650)],
        [(366,756),(1323,650)]
    ],
    2:[[(0,90),(1323,0)],
        [(0,225),(570,90)],
        [(571,385),(1323,90)],
        [(0,432),(569,226)],
        [(572,476),(1323,385)],
        [(0,756),(569,430)],
        [(570,536),(1323,474)],
        [(570,605),(1323,537)],
        [(570,673),(1323,606)],
        [(570,756),(1323,674)]
    ],
    3:[[(0,120),(1323,0)],
        [(0,415),(1323,121)],
        [(0,475),(1323,416)],
        [(0,543),(411,476)],
        [(412,543),(1323,476)],
        [(0,756),(412,543)],
        [(412,756),(1323,543)]
    ],
    4:[[(0,112),(1323,0)],
        [(0,756),(623,113)],
        [(623,378),(1323,113)],
        [(623,431),(1323,378)],
        [(623,494),(1323,431)],
        [(623,552),(1323,494)],
        [(623,619),(1323,552)],
        [(623,756),(1323,619)]
    ],
    5:[[(0,90),(1323,0)],
        [(0,756),(669,90)],
        [(669,227),(1323,90)],
        [(669,287),(1323,227)],
        [(669,378),(1323,287)],
        [(669,447),(1323,378)],
        [(669,756),(1323,447)]
    ],
    6:[[(0,90),(1323,0)],
        [(0,475),(1323,90)],
        [(0,538),(1323,475)],
        [(0,611),(366,538)],
        [(366,611),(1323,538)],
        [(0,756),(366,611)],
        [(366,756),(1323,611)]
    ],
    7:[[(0,60),(1323,0)],
        [(0,756),(646,60)],
        [(646,430),(1323,60)],
        [(646,492),(1323,430)],
        [(646,560),(1323,492)],
        [(646,623),(1323,560)],
        [(646,689),(1323,623)],
        [(646,756),(1323,689)]
    ],
    8:[[(0,75),(1323,0)],
        [(0,294),(1323,75)],
        [(0,543),(1323,294)],
        [(0,590),(1323,543)],
        [(0,648),(562,651)],
        [(562,648),(1323,590)],
        [(0,756),(562,648)],
        [(562,756),(1323,648)]
    ],
    10:[[(0,107),(1323,0)],
        [(0,557),(1323,107)],
        [(0,605),(1323,557)],
        [(0,658),(571,605)],
        [(569,658),(1323,605)],
        [(0,756),(569,658)],
        [(569,756),(1323,658)]
    ],
    11:[[(0,150),(1323,0)],
        [(0,462),(1323,150)],
        [(0,541),(1323,462)],
        [(0,627),(547,544)],
        [(547,627),(1323,541)],
        [(0,756),(547,627)],
        [(547,756),(1323,627)]
    ],
    12:[[(0,150),(1323,0)],
        [(0,756),(736,150)],
        [(736,347),(1323,150)],
        [(736,409),(1323,347)],
        [(736,483),(1323,409)],
        [(736,545),(1323,483)],
        [(736,605),(1323,545)]
    ]
}