#!/usr/bin/env python
# coding: utf-8

# In[10]:


def target_definition(df, nome_coluna, publico_alvo):

    import numpy as np

    df_trat = df

    # Variable to identify dismissal
    df_trat['desligado'] = [1 if x in ['Voluntário', 'Involuntário'] else 0 for
                            x in df.tipo_desligamento_classificação]

    # Transforming tipo_colaborador to what should be
    df_trat['tipo_colaborador'] = df_trat.tipo_colaborador.str.replace('NORMAL'
                                                                       , 'CLT')

    # Selecionando o público alvo
    df_trat = df_trat[df_trat[nome_coluna] == publico_alvo].drop(nome_coluna,
                                                                 axis=1).copy()

    # If it is active, dismissal equals today (in order to filter later)
    df_trat['datademissao'] = df_trat.datademissao.fillna(
        np.datetime64('today'))

    # Only considering business that were integrated to HR systems to avoid
    # missing/incorrect info, excluding Undergraduate that has a different 
    # behaviour

    df_trat = df_trat[(df_trat.integrada == 'Sim') &
                      (df.tipo_filial != 'UNDERGRADUATE')]

    return df_trat