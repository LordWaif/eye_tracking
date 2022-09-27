import os
from tqdm import tqdm
from config import ROOT_APPS
from makeTreeDir import OUTPUT_CSVTOFCSV,OUTPUT_TXTTOCSV,OUTPUT_FCSVTOFGRAPH
from pathlib import Path

def execToCsv():
    os.chdir(ROOT_APPS)
    txt_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.txt")
    txt_finders = list(txt_finders)
    bar = tqdm(total=len(txt_finders))
    for i in txt_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')

        cmd = "python3 toCsv.py "+input.__str__()+" -o "+output.__str__()
        #print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()
        bar.update(1)

def execFixacao():
    os.chdir(ROOT_APPS)
    csv_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.csv")
    def fill(elem):
        return not(elem.parts[-2]==OUTPUT_CSVTOFCSV)
    csv_finders = list(filter(fill,csv_finders))
    bar = tqdm(total=len(csv_finders))
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
    bar = tqdm(total=len(csv_finders))
    for i in csv_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_FCSVTOFGRAPH,i.stem+'.html')
        #print(input)
        #print(output)
        cmd = "python3 graficoFixacao.py "+input.__str__()+" -o "+output.__str__()
        #print(cmd)
        os.popen(cmd=cmd).read()
        bar.update(1)

def main():
    #createTree()
    #execToCsv()
    #execFixacao()
    execFGraph()

main()
