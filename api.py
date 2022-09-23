import os
from config import ROOT_APPS
from makeTreeDir import *
from pathlib import Path

def execToCsv():
    txt_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.txt")

    for i in txt_finders:
        input = i.absolute()
        output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')

        cmd = "python3 toCsv.py "+input.__str__()+" -o "+output.__str__()
        print("toCsv.py"+output.__str__()+'\n')
        os.popen(cmd=cmd).read()

def execFixacao():
    csv_finders = Path('/home/lordwaif/documents/dados_eyeTree').rglob("*.csv")
    for i in csv_finders:
        if i.parts[-2]==OUTPUT_CSVTOFCSV:
            continue
        input2 = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
        output2 = Path.joinpath(i.parent.parent.absolute(),OUTPUT_CSVTOFCSV,i.stem+'.csv')

        cmd = "python3 fixacao.py "+input2.__str__()+" -o "+output2.__str__()
        print("fixacao.py"+output2.__str__()+'\n')
        os.popen(cmd=cmd).read()

def main():
    os.chdir(ROOT_APPS)
    #createTree()
    execToCsv()
    #execFixacao()

main()
