import os,glob

from config import ROOT_DATA,ROOT_APPS
#Config
OUTPUT_TXTTOCSV = 'csv_structured'
OUTPUT_CSVTOFCSV = 'csv_fixacion'
OUTPUT_FCSVTOFGRAPH = 'fixacion_graph'
INPUT_CSVTOCSVHEAT = 'csv_heat'
OUTPUT_CSVTOHMGRAPH = 'heat_map_graph'
OUTPUT_NFIXTABLE = 'n_fix_table'
OUTPUT_SACADE = 'sacadas'
ACUMULADA = 'acumulada_graph'
ACUMULADA_DOTS = 'acumulada_graph_dots'
DEFAULT_DIRECTORIES = ['input_txt',
    OUTPUT_TXTTOCSV,
    OUTPUT_CSVTOFCSV,
    OUTPUT_FCSVTOFGRAPH,
    OUTPUT_CSVTOHMGRAPH,
    INPUT_CSVTOCSVHEAT,
    OUTPUT_NFIXTABLE,
    OUTPUT_SACADE,
    ACUMULADA,
    ACUMULADA_DOTS]


common_prefix = 'saeb'
comp = common_prefix

LAYER_2 = ['dados']
#LAYER_2 = [comp+'_2',comp+'_4']
#LAYER_1 = os.listdir('/home/lordwaif/documents/dados_eye/Coleta')
LAYER_1 = os.listdir('/home/lordwaif/documents/eye_leo/Entrega Piaui/')

BG_MAP = {
    comp+'_2':['4','5','6'],
    comp+'_4':['10','11','12']
}

main_dir = 'Coleta'

def createTreeDict():
    dirs = dict()
    for i in LAYER_1:
        dirs[i] = dict()
        for j in LAYER_2:
            dirs[i][j] = DEFAULT_DIRECTORIES
    return dirs

dirs = createTreeDict()

def cdCreate(path):
    if not(os.path.exists(path)):
        os.mkdir(path)
    os.chdir(path)

def createTree():
    os.chdir(ROOT_APPS)
    cdCreate(ROOT_DATA)
    cdCreate(main_dir)

    def recursive_createTree(dirs):
        for key,value in dirs.items():
            cdCreate(key)
            if type(value) == dict:
                recursive_createTree(value)
            else:
                for i in value:
                    if not(os.path.exists(i)):
                        os.mkdir(i)
            os.chdir('../')
    recursive_createTree(dirs)

def clearFolder(path):
    folders = glob.glob(path)
    for folder in folders:
        for file in os.listdir(folder):
            if file[::-1].split('.')[0][::-1] == 'txt':
                continue
            os.remove(os.path.join(folder,file))
            ...
#clearFolder("/home/lordwaif/documents/eye_leoTree/Coleta/*/dados/acumulada_graph_dots/")
#createTree()