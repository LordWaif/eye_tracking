import os,glob

from config import ROOT_DATA,ROOT_APPS
#Config
DEFAULT_DIRECTORIES = ['input_txt','csv_structured','csv_fixacion','fixacion_graph','heat_map_graph','csv_heat']
OUTPUT_TXTTOCSV = 'csv_structured'
OUTPUT_CSVTOFCSV = 'csv_fixacion'
OUTPUT_FCSVTOFGRAPH = 'fixacion_graph'
INPUT_CSVTOCSVHEAT = 'csv_heat'


common_prefix = 'saeb'
comp = common_prefix

LAYER_2 = [comp+'_2',comp+'_4']
LAYER_1 = os.listdir('/home/lordwaif/documents/dados_eyeTree/Coleta_2')

BG_MAP = {
    comp+'_2':['4','5','6'],
    comp+'_4':['10','11','12']
}

main_dir = 'Coleta_2'

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
    files = glob.glob(path)
    for f in files:
        os.remove(f)
#clearFolder('/home/lordwaif/documents/dados_eyeTree/Coleta_2/*/*/fixacion_graph/*')
#createTree()