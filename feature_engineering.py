#!/usr/bin/env python
# coding: utf-8

# In[10]:


def feature_engineering(df, months_ahead = 0):

    import numpy as np
    import pandas as pd

    df_trat = df

    # Unificando termos de raça

    df_trat['corraca_descricao'] = df_trat.corraca_descricao.str.replace('Preta/Negra','Negra').replace('Preta', 'Negra')

    # Tempo de casa
    
    if months_ahead == 0:
        df_trat['tempo_de_casa'] = ((df_trat.datademissao - df_trat.dataadmissao)/np.timedelta64(1, 'M'))
        
        # Overwrite ranges of months with company to predict
        evaluation_bins = [0, 24, 60, 120, 240, 999]
        group_names = [1, 2, 3, 4, 5]
        rngs_time = pd.cut(df_trat['tempo_de_casa'], bins=evaluation_bins,
                           labels=group_names, include_lowest=True, right=False)
        
        df_trat['ord_faixa_tempo_casa'] = rngs_time.tolist()
        
    

    '''
    Tipo Filial: Talvez sirva de ajuda para entender se digital, holding, etc
    tem mais propensão à Turnover.
    Vamos imputar com um valor dummy os que estão vazios.
    '''

    df_trat.tipo_filial = df_trat.tipo_filial.fillna('N_INFORMADO')

    return df_trat