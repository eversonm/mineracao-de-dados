import pandas as pd
import numpy as np
import glob  
import plotly.graph_objs as go
import plotly.offline as py
import matplotlib.pyplot as plt               # Visualização de dados
import matplotlib
plt.style.use('fivethirtyeight') 
import squarify
from datetime import datetime
from folium import Map
from folium.plugins import HeatMap

# FUNÇÃO PARA IMPORTAR DATASET

dir_path = "data/"

def importaData(files):
    
    data = dir_path + files
    allFiles = glob.glob('data/*.csv')
    list_ = []
    dtypes = {
        'ANO_BO': object,
        'NUM_BO': object,
        'DATAOCORRENCIA': object,
        'PERIDOOCORRENCIA':object,
        'BAIRRO':object,
        'CIDADE':object,
        'LATITUDE':object,
        'LONGITUDE':object,
        'LOGRADOURO':object,
        'DESCRICAOLOCAL':object,
        'DESCR_TIPO_VEICULO':object,
        'DELEGACIA_NOME': object,
        'QUANT_CELULAR': object
    }
    cols = ['ANO_BO', 'NUM_BO', 'DATAOCORRENCIA', 'PERIDOOCORRENCIA', 'BAIRRO', 'CIDADE', 'LATITUDE', 'LONGITUDE', 'LOGRADOURO', \
           'DESCRICAOLOCAL', 'DESCR_TIPO_VEICULO', 'DELEGACIA_NOME',  'QUANT_CELULAR']

    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0, delimiter=';', usecols=cols, dtype=dtypes, thousands=',')
        list_.append(df)

    df = pd.concat(list_, axis = 0, ignore_index = True)
    return df

# IMPORTANDO DATASET

dataset = importaData('*.csv')

# REMOVENDO DADOS DUPLICADOS

def removeDuplicados(df):
    df.drop_duplicates(subset=['DELEGACIA_NOME', 'ANO_BO', 'NUM_BO'], inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

dataset = removeDuplicados(dataset)

dataset['ANO_BO'] = pd.to_numeric(dataset['ANO_BO'], errors='coerce', downcast='integer')

dataset['NUM_BO'] = pd.to_numeric(dataset['NUM_BO'], errors='coerce', downcast='integer')

dataset['LATITUDE'] = dataset['LATITUDE'].replace({',':'.'}, regex=True)
dataset['LONGITUDE'] = dataset['LONGITUDE'].replace({',':'.'}, regex=True)

dataset['LATITUDE'] = pd.to_numeric(dataset['LATITUDE'], errors='coerce')
dataset['LONGITUDE'] = pd.to_numeric(dataset['LONGITUDE'], errors='coerce')

dataset['QUANT_CELULAR'] = pd.to_numeric(dataset['QUANT_CELULAR'], errors='coerce')

dataset.reset_index(drop='index',inplace=True)

# TRANSFORMANDO STRINGS PARA LOWER CASE

def lowerCase(df, cols):
    for col in cols:
        df[col] = df[col].str.title()
    
    return df

colsToLower = ["PERIDOOCORRENCIA", "LOGRADOURO", "BAIRRO", "DESCR_TIPO_VEICULO","CIDADE"]

all_data = lowerCase(dataset, colsToLower)

all_data = all_data[all_data['CIDADE']=='S.Paulo']

all_data.drop(686741, inplace=True)

all_data['datacorreta'] = pd.to_datetime(all_data['DATAOCORRENCIA'], format='%d/%m/%Y', errors = 'coerce')
all_data.drop(all_data[all_data['datacorreta'].isnull()].index, inplace=True)
all_data.drop(all_data[all_data['datacorreta']<'2010-01-01'].index, inplace=True)

import csv
all_data.to_csv('all_data.csv',index=False, doublequote=False, decimal='.', escapechar=' ', sep=',')
