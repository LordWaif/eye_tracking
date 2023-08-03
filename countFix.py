from config import REGIONS, DEFAULT_SEP_DF
import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Parametro para execução")

# obrigatorio
parser.add_argument('input-path', type=str, help='caminho para o arquivo csv')

# opcional
parser.add_argument('-o', '--output-name', default='region_output.csv',
                    type=str, required=False, help='nome do arquivo de saida')
args = vars(parser.parse_args())

PATH_IN = Path(args['input-path'])
OUTPUT_NAME = args['output_name']

contagem = ['arthur', 'gael', 'maria helena',
            'joão victor', 'desconhecido7', 'desconhecido9']
soma = ['pablo', 'leonardo']


def count(path_in=PATH_IN, path_out=OUTPUT_NAME):
    df = pd.read_csv(path_in, sep=DEFAULT_SEP_DF)
    qtd = 0
    total_ms_relevante = 0
    entrou = False
    for ch, val in REGIONS.items():
        name = Path(path_in).stem
        if path_in.stem.split('_')[-1] in contagem and path_in.stem[::-1].split('_', 1)[1][::-1] == "contagem_e_soma_material_completo":
            name = "contagem_material_completo"+"_"+path_in.stem.split('_')[-1]
        elif path_in.stem.split('_')[-1] in soma and path_in.stem[::-1].split('_', 1)[1][::-1] == "contagem_e_soma_material_completo":
            name = "soma_material_completo"+"_"+path_in.stem.split('_')[-1]
        if name.find(ch) == 0:
            entrou = True
            for j in val[0]['relevante']:
                inf_esq = j[0]
                sup_dir = j[1]
                range_x = [inf_esq[0], sup_dir[0]]
                range_y = [sup_dir[1], inf_esq[1]]
                df_region = df[(df['X'] >= range_x[0]) & (df['X'] <= range_x[1]) & (
                    df['Y'] >= range_y[0]) & (df['Y'] <= range_y[1])]
                qtd += len(df_region)
                total_ms_relevante += df_region['MS'].sum()
            break
    if (entrou):
        nao_relevante = len(df)-qtd
        total_ms_n_relevante = df['MS'].sum() - total_ms_relevante
        ret_dict = {'relevante': [qtd, total_ms_relevante/qtd, total_ms_relevante/1000], 'nao-relevante': [
            nao_relevante, total_ms_n_relevante/nao_relevante, total_ms_n_relevante/1000]}
        # print(path_out)
        pd.DataFrame(ret_dict).to_excel(path_out)
        return ret_dict


count()
