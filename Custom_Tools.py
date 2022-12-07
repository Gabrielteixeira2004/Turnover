#!/usr/bin/env python
# coding: utf-8

# In[10]:

import pandas as pd
import seaborn as sns
import numpy as np


class preprocess_afya:
    
    
    def __init__(self,df):
        '''
        Minimum structure of preprocess.
        
        Should be updated as many time as needed.
        
        Parameters
        ----------
        df: dataframe
            dataframe to be analyzed
        '''
        
        self.df = df

    def col_missing(self):
        '''
        Method that returns % of missing values in each column.
        
        Returns
        -------
        Pandas Series
            Column followed by the percentage of missing 
            (ie. 0.0 = no missing and 1.0 full missing)
        '''
        
        return self.df.isnull().mean()
    
    def row_missing(self):
        '''
        Method that returns % of missing values in each row.
        
        Returns
        -------
        pandas.core.series.Series
            Column followed by the percentage of missing 
            (ie. 0.0 = no missing and 1.0 full missing)
        '''
        
        return self.df.isnull().mean(axis=1)
    
    
    def cardinality(self):
        '''
        Method that returns cardinality (number of unique items) in each column.
        
        Returns
        -------
        Pandas Series
            Column followed by the cardinality.
            (ie. 0.0 = no missing and 1.0 full missing)
        '''
        
        return self.df.loc[:,self.df.dtypes == 'object'].nunique()
    
    
    def distribution(self, variables_analyze, output_variable):
        '''
        Method that returns the distribution comparing the output.
        
        Parameters
        ----------
        variables_analyze: list of strings
            variables that want to analyze.
        
        output_variable: string
            output variable that can reveal if there is underlying pattern.
        
        Returns
        -------
        plots of each variable considered
        '''

        
        for variable in variables_analyze:
            sns.displot(self.df, x=variable, hue=output_variable, kind="kde");
            
            
    
    def outlier_analyze(self, feature):
        
        '''
        Method using Sklearn's Isolation Forest that will analyze a dataset column and return 
        what is considered as an outlier.
        
        The only preprocess we will perform is notnull pandas filter.
        
        Parameter
        ----------
        feature: string
            Name of the columns that you want to analyze.
        
        
        Returns
        -------
        Pandas Dataframe
        
            Index
                Index of where this outlier was found.
                
            Column name
                Values of the column.
                
        '''
        
        

        from sklearn.ensemble import IsolationForest

        IForest = IsolationForest()

        df = self.df

        final_df = df.loc[df[feature].notnull(),feature]

        IForest.fit(final_df.values.reshape(-1,1));

        outlier_pred = IForest.predict(final_df .values.reshape(-1,1))

        df_analyze = pd.concat([final_df.reset_index(),pd.Series(outlier_pred,name='outlier')],axis=1)

        return df_analyze[df_analyze.outlier==-1].drop('outlier', axis=1)
    
    
    

    
class overfit:
    
    def __init__(self, X, y, models, scaler_insert = None, over_under_sample = None ):
        '''
        Tools to identify the trend of model overfit as soon as possible.
        
        Could use before feature selection or after, understand your business problem
        before using it.
        
        We are using train_test_split and you can choose if you want to scale or oversample.
        
        Should be updated as many time as needed.
        
        Parameters
        ----------
        X: dataframe
            dataframe without the target.
            
        y: series
            target.
            
        models: dictionary
            Composed by name of the model you want to use as key and
            the instantiated model as item.
            
            
        scaler_insert: object
            Choose the scaler you want to use in the process.
            Leave empty to not scale.
        
        over_under_sample: object
            Choose the oversample or undersample method you want to use in the process.
            Leave empty to not use it.
            
        '''

        from sklearn.model_selection import  train_test_split
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        self.models = models
        
        self.scaler_insert = scaler_insert
        
        self.over_under_sample = over_under_sample
        
        self.features = [col for col in X.columns]
     
        
    def overfit(self,sklearn_metric_score_function):
        
        '''
        Method that returns score for train and test score for some samples.
        
        Returns
        -------
        Pandas Dataframe
        
            Sample
                % of train or test considered
                
            Model
                Name of the model considered
                
            sklearn_metric_score_function
                Choose a sklearn score function that requires y_pred or y_prob
                arguments.
                
            Dataset
                If it is train dataset or test dataset
        '''
        
        import sklearn.metrics as mt
        
        import time
        
        Avaliacao = pd.DataFrame()
        
        training_start = time.time()
        
        for sample in np.arange(0.2, 1.1, 0.2):
            
            sample_start = time.time()

            sample_train_n = int(len(self.X_train)*sample)
            sample_test_n = int(len(self.X_test)*sample)

            sample_train_X = self.X_train[:sample_train_n].copy()
            sample_train_y = self.y_train[:sample_train_n].copy()
            sample_test_X = self.X_test[:sample_test_n].copy()
            sample_test_y = self.y_test[:sample_test_n].copy()

            print(f'\nAmount of sample fitted and predicted on train set: {sample_train_n}')
            print(f'Amount of sample predicted on test set: {sample_test_n}')
            print(f'Sample {sample*100:.0f}% generated \n')
            
            if self.scaler_insert is not None:
                scaler = self.scaler_insert

                sample_train_X[self.features] = scaler.fit_transform(sample_train_X[self.features])
                sample_test_X[self.features] = scaler.transform(sample_test_X[self.features])
                
                name_scaler = ' - '+type(scaler).__name__
                
            else:
                
                name_scaler = ''
                
                
                
            if self.over_under_sample is not None:
                
                over_under = self.over_under_sample
                
                sample_train_X,sample_train_y = over_under.fit_resample(sample_train_X,sample_train_y)

                name_over_under_sample = ' - ' + type(over_under).__name__
                
            else:
                
                name_over_under_sample = ''
                
                
            for name_model,model in self.models.items():
                
                model_start = time.time()


                model.fit(sample_train_X,sample_train_y)
                
                
                
                if 'y_pred' in sklearn_metric_score_function.__code__.co_varnames:
                    
                    score_train = sklearn_metric_score_function(sample_train_y,model.predict(sample_train_X))
                    
                    score_test = sklearn_metric_score_function(sample_test_y,model.predict(sample_test_X))
                    
                    
                else:
                    
                    print('Score function selected does not have y_pred (final output)')



                resultado = {
                    'Sample' : sample,
                    'Model' : name_model+ name_scaler + name_over_under_sample,
                    sklearn_metric_score_function.__name__: score_train,
                    'Dataset' : 'Train'
                }

                Avaliacao = pd.concat([Avaliacao,pd.DataFrame(resultado, index=[0])])

                resultado = {
                    'Sample' : sample,
                    'Model' : name_model+name_scaler + name_over_under_sample,
                    sklearn_metric_score_function.__name__: score_test,
                    'Dataset' : 'Test'
                }

                Avaliacao = pd.concat([Avaliacao,pd.DataFrame(resultado, index=[0])])
                
                elapsed_time = time.time() - model_start

                print(name_model+ name_scaler + name_over_under_sample+': ' + str(int(elapsed_time)) + " seconds")
            
            
            elapsed_time_sample = time.time() - sample_start
            
            print('\nTotal sample training time: ' + str(int(elapsed_time_sample)) + " seconds\n")
            
        elapsed_time_sample = time.time() - training_start
            
        print('\nTotal training time: ' + str(int(elapsed_time_sample)) + " seconds\n")
                
        return Avaliacao
    
  


def feature_selection(X, y, algorithms, iterations=5):

    from timeit import default_timer as timer
    
    from sklearn.feature_selection import SelectKBest

    init_time = timer()

    Kbest_all = pd.DataFrame()

    for iteration in range(0, iterations):

        it_time = timer()

        print('Iteration: ' + str(iteration+1))

        Kbest_it = pd.DataFrame()

        for algorithm in algorithms:

            K = SelectKBest(algorithm, k=X.shape[1]//3)

            K.fit(X, y.values.ravel())

            resultado = pd.DataFrame(data=zip(X.columns, K.get_support()), columns=['Columns', algorithm.__name__+'_Kbest'])

            if Kbest_it.empty:
                Kbest_it = resultado

            else:
                Kbest_it = pd.merge(Kbest_it, resultado, on='Columns')

        if Kbest_all.empty:
            Kbest_all = Kbest_it
        else:
            Kbest_all = pd.concat([Kbest_all, Kbest_it])

        now = timer()

        print('Total iteration time: '+str(round(now - it_time, 0))+' seconds.\n')

    Kbest_all['Total_points'] = Kbest_all.drop('Columns', axis=1).sum(axis=1)

    print('\nTotal operation time: ' + str(round((now - init_time)/60, 2))+' minutes.')

    return Kbest_all.sort_values('Total_points', ascending=False)
    