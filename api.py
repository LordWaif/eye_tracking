from ast import In
import os
from sys import stdout
from tqdm import tqdm
from config import GRAPH_TITLE_DEFAULT, IMAGE_NAME_PREFFIX, IMAGE_NAME_SUFFIX, IMAGE_PATH, PATH_N_FIX_TABLE, ROOT_APPS, TEMPORAY_COMPACT_FOLDER, VIRTUAL_ENVIROMENT
from makeTreeDir import INPUT_CSVTOCSVHEAT,OUTPUT_CSVTOFCSV, OUTPUT_CSVTOHMGRAPH,OUTPUT_TXTTOCSV,OUTPUT_FCSVTOFGRAPH,BG_MAP,OUTPUT_NFIXTABLE,INPUT_CSVTOCSVHEAT,OUTPUT_SACADE,main_dir, cdCreate,createTree,clearFolder
from pathlib import Path
import re

SEARCH_DATA_PATH = '/home/lordwaif/documents/eye_leoTree'
#REGEXP_MAP_WITH_BG = '.*atv_(\d)_.*'
REGEXP_MAP_WITH_BG = 'V[ií]deo (\d)\.'

def execToCsv():
    os.chdir(ROOT_APPS)
    txt_finders = Path(SEARCH_DATA_PATH).rglob("*.txt")
    txt_finders = list(txt_finders)
    bar = tqdm(total=len(txt_finders),desc="run_task={}".format("Gerando csv's"))
    for i in txt_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')

        cmd = "python3 toCsv.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        #print(cmd)
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...

def execFixacao():
    os.chdir(ROOT_APPS)
    csv_finders = Path(SEARCH_DATA_PATH).joinpath(main_dir).rglob("*.csv")
    def fill(elem):
        return not(elem.parts[-2]==OUTPUT_CSVTOFCSV)
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando fixações'))
    for i in csv_finders:
        input = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOFCSV,i.stem+'.csv')

        cmd = "python3 fixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        #print(input)
        #print("fixacao.py"+output2.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...

def execFGraph():
    os.chdir(ROOT_APPS)
    csv_finders = Path(SEARCH_DATA_PATH).rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==OUTPUT_CSVTOFCSV
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format('gerando graficos'))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        match = re.match(re.compile(REGEXP_MAP_WITH_BG),input.stem)
        bg_command = ''
        titulo = GRAPH_TITLE_DEFAULT
        if match:
            #bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+BG_MAP[input.parts[-3]][int(match.groups()[0])]+IMAGE_NAME_SUFFIX)
            bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+match.groups()[0]+IMAGE_NAME_SUFFIX)
            bg_command = " -bg '"+bg_path+"' "
            #output = Path.joinpath(output.parent,output.stem+output.parts[-4]+"_q"+BG_MAP[input.parts[-3]][int(match.groups()[0])]+output.suffix)
            output = Path.joinpath(output.parent,output.stem+output.parts[-4]+output.suffix)
            #titulo = output.parts[-4]+' Questão '+BG_MAP[input.parts[-3]][int(match.groups()[0])]
            titulo = output.parts[-4]+' ,'+re.sub('V[ií]deo \d\. ','',output.stem).replace('_atv_0_','')
        cmd = "python3 graficoFixacao.py '"+input.__str__()+"' -o '"+output.__str__()+"'"+bg_command+" -tbg '"+titulo+"'"
        #print(cmd)
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...

#from functools import reduce
def compactAll(directory = TEMPORAY_COMPACT_FOLDER):
    cdCreate(directory)
    '''
    def concat(x, y):
        return x.__str__() + ' ' + y.__str__()
    '''
    graph_finders = list(Path(SEARCH_DATA_PATH).rglob("*.html"))
    graph_heat_finders = list(Path(SEARCH_DATA_PATH).rglob("*.png"))
    def fill(elem):
        return elem.parts[-2]==OUTPUT_CSVTOHMGRAPH
    graph_heat_finders = list(filter(fill,graph_heat_finders))
    graphs = [graph_finders,graph_heat_finders]
    titulo_arquivo = {0:'Fixacoes',1:'HeatMap'}
    #graph_finders = reduce(concat,graph_finders)
    #cmd = 'tar -zcf teste.tar.gz '+graph_finders
    os.chdir('../')
    for ind,graph_list in enumerate(graphs):
        bar = tqdm(total=len(graph_list),desc="run_task={}".format('copying...'))
        for i in graph_list:
            cmd = "cp '"+i.__str__()+"' '"+os.path.join(TEMPORAY_COMPACT_FOLDER,i.name)+"'"
            #print(cmd)
            os.popen(cmd=cmd).read()
            bar.update(1)
        
        cmd = "tar -zvcf '"+titulo_arquivo[ind]+".tar.gz' '"+Path(directory).name+"/'"
        import subprocess,sys
        t = tqdm(total=len(graph_list),desc="run_task={}".format("comprimindo.."))
        process = subprocess.Popen(cmd, shell=True, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        for line in process.stdout:
            t.update(1)
            sys.stdout.flush()
        process.stdout.close()
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)
        clearFolder(directory)
    ...

def execInputHeatMap():
    os.chdir(ROOT_APPS)
    csv_finders = Path(SEARCH_DATA_PATH).rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==OUTPUT_TXTTOCSV
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Gerando csv's para HeatMap"))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),INPUT_CSVTOCSVHEAT,i.stem+'.csv')

        cmd = "python3 toCsv.py '"+input.__str__()+"' -o '"+output.__str__()+"' -hm True"
        #print(cmd)
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)
    ...

def createvEnviroment():
    if not(os.path.exists(VIRTUAL_ENVIROMENT)):
        os.popen('virtualenv '+VIRTUAL_ENVIROMENT+' --python=python2.7')
    p_enviroment = Path(VIRTUAL_ENVIROMENT)
    #os.popen('source '+p_enviroment.name+'/bin/activate')
    #deactivate
    ...

def execHeatMap():
    os.chdir(ROOT_APPS)
    csv_finders = Path(SEARCH_DATA_PATH).rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==INPUT_CSVTOCSVHEAT
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Gerando graficos de HeatMap"))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOHMGRAPH,i.stem+'.png')
        match = re.match(re.compile(REGEXP_MAP_WITH_BG),input.stem)
        bg_command = ''
        titulo = GRAPH_TITLE_DEFAULT
        if match:
            #bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+BG_MAP[input.parts[-3]][int(match.groups()[0])]+IMAGE_NAME_SUFFIX)
            bg_path = os.path.join(IMAGE_PATH,IMAGE_NAME_PREFFIX+match.groups()[0]+IMAGE_NAME_SUFFIX)
            bg_command = " -b '"+bg_path+"' "
            #output = Path.joinpath(output.parent,output.stem+output.parts[-4]+"_q"+BG_MAP[input.parts[-3]][int(match.groups()[0])]+output.suffix)
            output = Path.joinpath(output.parent,output.stem+output.parts[-4]+output.suffix)
            #titulo = output.parts[-4]+' Questão '+BG_MAP[input.parts[-3]][int(match.groups()[0])]
            titulo = output.parts[-4]+' ,'+re.sub('V[ií]deo \d\. ','',output.stem).replace('_atv_0_','')
        os.popen("python3 gazeheatplot.py '"+str(input)+"' 1920 1080 -a 0.6 -o '"+str(output)+"'"+bg_command).read()
        bar.update(1)
    ...
from config import DEFAULT_ENCODING,DEFAULT_SEP_DF,REGIONS,SCREEN_H,SCREEN_W
import pandas as pd
def countRegions():
    os.chdir(ROOT_APPS)
    graph_finders = Path(SEARCH_DATA_PATH).rglob("*.html")
    dados = []
    for i in graph_finders:
        input = i.absolute()
        match = re.match(re.compile('.*q(\d{1,2}).*'),input.stem)
        match_name = re.match(re.compile('(.*_atv_(\d)_).*'),input.stem)
        if match and match_name:
            q = match.groups()[0]
            nome_arq = match_name.groups()[0]+'.csv'
            lista = REGIONS[int(q)]
            for j in range(0,len(lista)):
                proporcao_x = SCREEN_W/1323
                proporcao_y = SCREEN_H/756
                xl = lambda x: int(x*proporcao_x)
                yl = lambda y: int(y*proporcao_y)
                inf_e = lista[j][0]
                sup_d = lista[j][1]
                df = pd.read_csv(Path.joinpath(input.parent.parent,OUTPUT_CSVTOFCSV,nome_arq),sep=DEFAULT_SEP_DF,encoding=DEFAULT_ENCODING)
                df = df[df['X']>xl(inf_e[0])]
                df = df[df['Y']<yl(inf_e[1])]
                df = df[df['X']<xl(sup_d[0])]
                df = df[df['Y']>yl(sup_d[1])]
                fix_per_reg = df
                dados.append([i.parts[-3],re.match(re.compile('.*atv_\d_(.*)_q'),i.stem).groups()[0],q,j+1,fix_per_reg.shape[0]])
    resultado = pd.DataFrame(dados,columns=['Saeb','Aluno','Questao','Regiao','Quantidade_Fixacoes'])
    resultado.to_csv(os.path.join(PATH_N_FIX_TABLE,'resultados_nfix.csv'),sep=';',index=False)
    ...

def countRegionsL():
    os.chdir(ROOT_APPS)
    graph_finders = Path(SEARCH_DATA_PATH).rglob("*.html")
    dados = []
    for i in graph_finders:
        input = i.absolute()
        match = re.match(re.compile('.*q(\d{1,2}).*'),input.stem)
        match_name = re.match(re.compile('(.*_atv_(\d)_).*'),input.stem)
        if match and match_name:
            q = match.groups()[0]
            nome_arq = match_name.groups()[0]+'.csv'
            lista = REGIONS[int(q)]
            for j in range(0,len(lista)):
                proporcao_x = SCREEN_W/1323
                proporcao_y = SCREEN_H/756
                xl = lambda x: int(x*proporcao_x)
                yl = lambda y: int(y*proporcao_y)
                inf_e = lista[j][0]
                sup_d = lista[j][1]
                df = pd.read_csv(Path.joinpath(input.parent.parent,OUTPUT_CSVTOFCSV,nome_arq),sep=DEFAULT_SEP_DF,encoding=DEFAULT_ENCODING)
                df = df[df['X']>xl(inf_e[0])]
                df = df[df['Y']<yl(inf_e[1])]
                df = df[df['X']<xl(sup_d[0])]
                df = df[df['Y']>yl(sup_d[1])]
                fix_per_reg = df
                dados.append([i.parts[-3],re.match(re.compile('.*atv_\d_(.*)_q'),i.stem).groups()[0],q,j+1,fix_per_reg.shape[0]])
    resultado = pd.DataFrame(dados,columns=['Saeb','Aluno','Questao','Regiao','Quantidade_Fixacoes'])
    resultado.to_csv(os.path.join(PATH_N_FIX_TABLE,'resultados_nfix.csv'),sep=';',index=False)
    ...

def fload():
    for i in Path('/home/lordwaif/documents/eye_leo').rglob("*.txt"):
        cmd = "cp '"+i.__str__()+"' '"+Path(SEARCH_DATA_PATH).joinpath(main_dir).joinpath(i.parts[-2],'dados/input_txt').__str__()+"'"
        print(cmd)
        os.popen(cmd)

def sacade():
    csv_finders = Path(SEARCH_DATA_PATH).rglob("*.csv")
    def fill(elem):
        return elem.parts[-2]==OUTPUT_TXTTOCSV
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders),desc="run_task={}".format("Calculando numero de sacadas"))
    r = []
    for i in csv_finders:
        input = i
        output = i.parent.parent.joinpath(OUTPUT_SACADE)
        cmd = "python3 sacadasCalc.py '"+input.__str__()+"' -o '"+output.__str__()+"'"
        res = os.popen(cmd).read()
        r.append(input.parts[-4]+' | '+input.parts[-1]+' | Sacadas Qtd: '+str(res))
        with open(input.parent.parent.joinpath(OUTPUT_NFIXTABLE,'numero.txt').__str__(),'w',encoding='utf-8') as file:
            file.write(str(res))
            file.close()
        bar.update(1)
    with open('numero_de_sacadas.txt','w') as f:
        f.writelines(r)
    ...

def main():
    #createTree()
    #fload()
    #execToCsv()
    #execFixacao()
    #execFGraph()
    #execInputHeatMap()
    #createvEnviroment()
    #execHeatMap()
    #compactAll()
    #countRegionsL()
    sacade()
    ...

if __name__ == '__main__':
    main()
    ...
