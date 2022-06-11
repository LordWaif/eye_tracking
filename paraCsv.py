import pandas as pd

PATH = "video_1_multiplicacao"
arquivo = []
with open(PATH+'.txt','r',encoding='utf-8') as file:
    arquivo = file.readlines()
    file.close()

arquivo = [arquivo[i].split(',') for i in range(len(arquivo))]
excluidos = []
for i in range(len(arquivo)):
    if(arquivo[i][0] == '0' or len(arquivo[i])<4):
        excluidos.append(arquivo[i])
        continue
    for j in range(len(arquivo[i])):
        arquivo[i][j] = arquivo[i][j].replace('(','')
        arquivo[i][j] = arquivo[i][j].replace(')','')
        arquivo[i][j] = arquivo[i][j].replace('\n','')
        if arquivo[i][j].count('_')>1:
            arquivo[i][j] = arquivo[i][j].replace('_','/',2)
            arquivo[i][j] = arquivo[i][j].replace('_',':',2)
            arquivo[i][j] = arquivo[i][j].replace('.',':',1)
        else:
            arquivo[i][j] = arquivo[i][j].replace(' ','')
        if(arquivo[i][j] == 'NaN'): arquivo[i][j] = None
        try:
            arquivo[i][j] = float(arquivo[i][j])
        except:
            pass
i=0
while i<len(excluidos):
    arquivo.remove(excluidos[i])    
    i+=1

df = pd.DataFrame(arquivo)
df.columns = ['CLASSE','INDICE','DATE_TIME','X_TELA','Y_TELA','X_MOUSE','Y_MOUSE','V1','V2','V3','V4','V5','V6','V7','NOME']
df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format="%Y/%m/%d %H:%M:%S:%f")
df.to_csv(PATH+'.csv',sep=';',encoding='utf-8')