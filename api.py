import os
from makeTreeDir import *
from pathlib import Path

txt_finders = Path('../dados_eyeTree').rglob('*.txt')

#createTree()
for i in txt_finders:
    #python3 toCsv.py ./input -o ./output/saida.csv -m true
    #base_path = i.parent.parent.absolute()
    input = i.absolute()
    output = Path.joinpath(i.parent.parent.absolute(),OUTPUT_TXTTOCSV,i.stem+'.csv')
    cmd = "python3 toCsv.py "+input.__str__()+" -o "+output.__str__()
    # python3 toCsv.py /home/lordwaif/documents/eye_tracking/../dados_eyeTree/Coleta_2/coleta_maio/saeb_2/input_txt/2021_10_14_08_28_34_392_dados.txt -o ./saida.csv
    print('\n\n'+cmd+'\n\n')
    os.popen(cmd=cmd).read()