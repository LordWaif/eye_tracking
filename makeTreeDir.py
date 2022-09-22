import os

from config import ROOT_DATA
DEFAULT_DIRECTORIES = ['input_txt','csv_structured']
OUTPUT_TXTTOCSV = 'csv_structured'


common_prefix = 'saeb'
comp = common_prefix

LAYER_2 = [comp+'_2',comp+'_4']
LAYER_1 = os.listdir('/home/lordwaif/documents/dados_eye/')

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
    os.mkdir(path)
    os.chdir(path)

def createTree():
    if not(os.path.exists(ROOT_DATA)):
        os.makedirs(ROOT_DATA)

    os.chdir(ROOT_DATA)
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

#createTree()