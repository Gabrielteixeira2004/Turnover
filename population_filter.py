#!/usr/bin/env python
# coding: utf-8

# In[10]:


def population_filter(df):

    '''
    Filter population to predict
    '''

    df_trat = df

    # Dismissal with one year or less and Voluntary Attrition
    df_trat = df_trat[(df_trat['datademissao'] > '2021-10-01')]

    df_trat = df_trat[(df_trat.tipo_desligamento_classificação == 'Voluntário')
                      | (df_trat.tipo_desligamento_classificação.isnull())]

    return df_trat
