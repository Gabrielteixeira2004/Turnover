#!/usr/bin/env python
# coding: utf-8

# In[10]:

def scale_dataset(df,features, scaler):
    
    '''
    The main objective is to avoid feature missing from analyzed dataset that made one-hot encoding
    '''

    feature_missing = [x for x in features if x not in df.columns.tolist()]

    for missing in feature_missing:

        df[missing] = 0

    if scaler is not None:
        df[features] = scaler.transform(df[features])
    
    df = df[features]

    return df
