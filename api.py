import os
from sys import stdout
from tqdm import tqdm
from config import GRAPH_TITLE_DEFAULT, IMAGE_NAME_PREFFIX, IMAGE_NAME_SUFFIX, IMAGE_PATH, ROOT_APPS, TEMPORAY_COMPACT_FOLDER, VIRTUAL_ENVIROMENT
from makeTreeDir import OUTPUT_CSVTOFCSV,OUTPUT_TXTTOCSV,OUTPUT_FCSVTOFGRAPH,BG_MAP,INPUT_CSVTOCSVHEAT, cdCreate,createTree
from pathlib import Path
import re

def execToCsv():
    os.chdir(ROOT_APPS)
    txt_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.txt")
    txt_finders = list(txt_finders)
    bar = tqdm(total=len(txt_finders),desc="run_task={}".format("Gerando csv's"))
    for i in txt_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')

        cmd = "python3 toCsv.py "+input.__str__()+" -o "+output.__str__()
        #print(cmd)
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)

def execFixacao():
    os.chdir(ROOT_APPS)
    csv_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.csv")
    def fill(elem):
        return not(elem.parts[-2]==OUTPUT_CSVTOFCSV)
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando fixações'))
    for i in csv_finders:
        input = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOFCSV,i.stem+'.csv')

        cmd = "python3 fixacao.py "+input.__str__()+" -o "+output.__str__()
        #print("fixacao.py"+output2.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==OUTPUT_CSVTOFCSV
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        match = re.match(re.compile('.*atv_(\d)_.*'),input.stem)
        bg_command = ''
        titulo = GRAPH_TITLE_DEFAULT
        if match:
            bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+BG_MAP[input.parts[-3]][int(match.groups()[0])]+IMAGE_NAME_SUFFIX)
            bg_command = " -bg "+bg_path
            output = Path.joinpath(output.parent,output.stem+output.parts[-4]+"_q"+BG_MAP[input.parts[-3]][int(match.groups()[0])]+output.suffix)
            titulo = output.parts[-4]+' Questão '+BG_MAP[input.parts[-3]][int(match.groups()[0])]
        cmd = "python3 graficoFixacao.py "+input.__str__()+" -o "+output.__str__()+bg_command+" -tbg '"+titulo+"'"
        #print(cmd)
        os.popen(cmd=cmd).read()
        bar.update(1)

#from functools import reduce
def compactAll(directory = TEMPORAY_COMPACT_FOLDER):
    cdCreate(directory)
    '''
    def concat(x, y):
        return x.__str__() + ' ' + y.__str__()
    '''
    graph_finders = list(Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.html"))
    #graph_finders = reduce(concat,graph_finders)
    #cmd = 'tar -zcf teste.tar.gz '+graph_finders
    bar = tqdm(total=len(graph_finders),desc="run_task={}".format('copying...'))
    for i in graph_finders:
        cmd = 'cp '+i.__str__()+' '+i.name
        os.popen(cmd=cmd).read()
        bar.update(1)
    os.chdir('../')
    bar.close()
    
    cmd = 'tar -zvcf teste.tar.gz '+Path(directory).name+'/'
    import subprocess,sys
    t = tqdm(total=len(graph_finders),desc="run_task={}".format("comprimindo.."))
    process = subprocess.Popen(cmd, shell=True, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    for line in process.stdout:
        t.update(1)
        sys.stdout.flush()
    process.stdout.close()
    return_code = process.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)

def execInputHeatMap():
    os.chdir(ROOT_APPS)
    csv_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==OUTPUT_TXTTOCSV
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Gerando csv's para HeatMap"))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),INPUT_CSVTOCSVHEAT,i.stem+'.csv')

        cmd = "python3 toCsv.py "+input.__str__()+" -o "+output.__str__()+" -hm True"
        #print(cmd)
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)

def createvEnviroment():
    if not(os.path.exists(VIRTUAL_ENVIROMENT)):
        os.popen('virtualenv '+VIRTUAL_ENVIROMENT+' --python=python2.7')
    p_enviroment = Path(VIRTUAL_ENVIROMENT)
    os.popen('source '+p_enviroment.name+'/bin/activate')
    #deactivate
    ...




def main():
    #createTree()
    #execToCsv()
    #execFixacao()
    #execFGraph()
    #compactAll()
    #execInputHeatMap()
    createvEnviroment()
    ...

main()
