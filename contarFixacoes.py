import pandas as pd
from makeTreeDir import OUTPUT_CSVTOFCSV
from pathlib import Path

PATH_RAW_REAL_EYE = Path('/home/lordwaif/documents/usecase_andiara/').joinpath(OUTPUT_CSVTOFCSV)

archives = PATH_RAW_REAL_EYE.glob('*.csv')
registro = dict()
quantidades,caminhos = [],[]
for arq in archives:
    quantidades.append(len(open(arq).readlines())-1)
    caminhos.append(arq.stem)

registro['ARQUIVOS'] = caminhos
registro['QUANTIDADE_FIXACOES'] = quantidades

#pd.DataFrame(registro).to_csv('quantidades.csv',index=False)
pd.DataFrame(registro).to_excel('quantidades.xlsx')