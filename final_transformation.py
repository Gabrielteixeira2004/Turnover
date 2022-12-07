#!/usr/bin/env python
# coding: utf-8

# In[10]:


def final_transformation(df, features, months_ahead=0, apply_scale='Y'):

    '''
    Apply all custom functions to transform the Test and Holdout datasets 
    '''

    from feature_engineering import feature_engineering
    from drop_turnover import drop_turnover
    from preprocess_turnover import preprocess_turnover
    from scale_dataset import scale_dataset
    from pickle import load

    df_trat = preprocess_turnover(
        drop_turnover(
            feature_engineering(
                df, months_ahead
            )
        )
    )

    if apply_scale == 'Y':
        scaler = load(open('Scaler.pkl', 'rb'))
    else:
        scaler = None

    df_trat = scale_dataset(
        df_trat, features, scaler)

    return df_trat
