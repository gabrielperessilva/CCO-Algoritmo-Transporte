import pandas as pd
import numpy as np
import sys

def verificaTabelaCustos(nome):
    df = pd.read_excel(nome)

    indices_coluna = df.columns.tolist()
    if indices_coluna != ['Envio', 'Chegada', 'Custo']:
            print("Os índices da coluna não correspondem a 'Envio', 'Chegada' e 'Custo'.")
            sys.exit()

    num_linhas_por_coluna = df.count()
    if num_linhas_por_coluna.nunique() != 1:
        print("As colunas têm números diferentes de linhas.")
        sys.exit()

    serie_numerica = pd.to_numeric(df['Custo'], errors='coerce')
    if not(serie_numerica.notnull().all()):
        print("A coluna Custo não é composta apenas por números.")
        sys.exit()

def verficaTabelaOD(nome):
    df = pd.read_excel(nome)

    indices_coluna = df.columns.tolist()
    if indices_coluna != ['Unnamed: 0', 'Oferta', 'Demanda']:
            print("Os índices da coluna não correspondem a 'Unnamed: 0', 'Oferta', 'Demanda'.")
            sys.exit()

    for index, row in df.iterrows():
        if(pd.isnull(row['Demanda']) and pd.isnull(row['Oferta'])):
            print("Celulas incompletas")
            sys.exit()
        for index2, row2 in df.iterrows():
            if(index != index2):
                if(row2['Unnamed: 0'] == row['Unnamed: 0']):
                    print('Ofertante ou demandante repetido') 
                    sys.exit()   

def criar_tabela(nome1, nome2):
    verficaTabelaOD(nome1)
    verificaTabelaCustos(nome2)
    # Carregar a planilha do Excel em um DataFrame
    df = pd.read_excel(nome1)
    temp = pd.DataFrame()
    temp[''] = ''

    i = 1
    for index, row in df.iterrows():
        if not(pd.isnull(row['Demanda']) or pd.isnull(row['Oferta'])):
            temp.at[i, ''] = row['Unnamed: 0']
            i+=1
            temp[row['Unnamed: 0']] = np.nan
        elif pd.isnull(row['Demanda']):
            temp.at[i, ''] = row['Unnamed: 0']
            i+=1
        else:
            temp[row['Unnamed: 0']] = np.nan

    temp.at[i, ''] = "Demanda"
    temp['Oferta'] = np.nan
    soma = max(df['Oferta'].sum(), df['Demanda'].sum())

    i = 1
    for index, row in df.iterrows():
        if not(pd.isnull(row['Demanda']) or pd.isnull(row['Oferta'])):
            temp.at[i, 'Oferta'] = soma
            i+=1
            temp.loc[temp.index[-1], row['Unnamed: 0']] = soma
        elif pd.isnull(row['Demanda']):
            temp.at[i, 'Oferta'] = row['Oferta']
            i+=1
        else:
            temp.loc[temp.index[-1], row['Unnamed: 0']] = row['Demanda']

    temp.iloc[-1, -1] = temp.iloc[-1, 1:].sum() - temp['Oferta'].sum()


    custos = pd.read_excel(nome2)
    bigM = int(max(custos['Custo'].dropna())) * 50
    bigM = 500
    temp = temp.fillna(bigM)
    for index, row in custos.iterrows():
        for index2, row2 in temp.iterrows():
            if(row['Envio'] == row2['']):
                temp.loc[index2, row['Chegada']] = row['Custo']
                

    for index, row in temp.iterrows():
        if (row[''] in temp.columns):
            temp.loc[index, row[''] ]= 0

    temp.to_excel("tabelas/custos.xlsx", index=False)