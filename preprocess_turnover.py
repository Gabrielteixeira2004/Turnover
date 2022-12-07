#!/usr/bin/env python
# coding: utf-8

# In[10]:


def preprocess_turnover(df):
    import pandas as pd
    import re

    '''
    Ordinal Encoding: escolaridade_classificação, agrup_salario.

    One-Hot Encoding: corraca_descricao, genero, VP_descricao, tipo_filial

    '''
    df_ord = df

    df_ord['escolaridade_classificação'] = df_ord['escolaridade_classificação'].map(
        {'Não declarado': 0,
         'Até Ensino Médio Completo': 1,
         'Ensino Superior Completo': 2,
         'Pós-Graduação Completa': 3,
         'Mestrado Completo': 4,
         'Doutorado ou Acima': 5}
    )

    df_hot = pd.get_dummies(df_ord)

    '''
    Imputing nulls
    Idade: Average
    ord_faixa_etaria: Corresponding Idade
    '''

    df_hot['idade'] = df_hot['idade'].fillna(39)
    df_hot['ord_faixa_etaria'] = df_hot['ord_faixa_etaria'].fillna(3.0)

    '''
    Taking out some hots that are from system's gap of information
    '''

    drop = ['VP_descricao_VP NAO ENCONTRADA', 'corraca_descricao_Não Informado',
            'genero_Não Informado', 'tipo_filial_N_INFORMADO']

    final_drop = [x for x in df_hot.columns if x not in drop]

    df_hot = df_hot[final_drop]

    df_hot = df_hot.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '', x))

    return df_hot