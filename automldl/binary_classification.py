import copy
import multiprocessing
import numpy as np
from sklearn.base import BaseEstimator
import joblib
import pandas as pd


class Auto_Estimator(BaseEstimator):
    '''
    This class takes the arguments as

    data:This argument takes the dataset path
    target:This argument takes the target value of the dataset

    '''

    def __init__(
        self,
        data,
        target,
        time_left_for_this_task=3600,
        seed=1,
        n_jobs=-1,
        metric=None,
    ):
        self.data = data
        self.target = target
        self.time_left_for_this_task = time_left_for_this_task
        self.seed = seed
        self.n_jobs = n_jobs
        self.metric = metric

        try:
            self.data = pd.read_csv(self.data)
            self.target = self.data[self.target]

        except Exception as e:
            print('Exception caught is:',e)        


    def numerical_columns(self):
        numeric_list = list()
        
        for i in list(self.data.columns):
            if self.data[i].dtypes != 'object':
                numeric_list.append(i)

        return numeric_list           

    def categorical_columns(self):
        categorical_list = list()
        
        for i in list(self.data.columns):
            if self.data[i].dtypes == 'object':
                categorical_list.append(i)

        return categorical_list


    def Name_of_Target_Variable(self):
        
        return self.target
    
    def data_shape(self):
        
        return self.data.shape
    
    def length_of_dataframe(self):
        
        return self.data.shape[0]
    
    def binary_columns(self):
        
        binary_list = list()

        try:
            for i in list(self.data.columns):
                if len(self.data[i].unique()) == 2:
                    binary_list.append(i)
                
            return binary_list   
        except Exception as e:
            print('Exception caught is',e)

    def Ternary_columns(self):
         
        Ternary_list = list()
        try:
            for i in list(self.data.columns):
                if len(self.data[i].unique()) == 3:
                    Ternary_list.append(i)
        
            return Ternary_list   
        except Exception as e:
            print('Exception caught is',e)



    def describe_data(self):
        try:
            vars = ['number of numerical columns', 'number of categorical columns', 'Target Column', 'shape of the dataframe', 'size of dataframe', 'binary columns',
                    'ternary columns']

            cols = ['Description', 'Count']

            df = pd.DataFrame(columns=cols)

            #df.loc[0] = [vars[0], len(self.check_for_Nan_values())]
            df.loc[0] = [vars[0], len(self.numerical_columns())]
            df.loc[1] = [vars[1], len(self.categorical_columns())]
            df.loc[2] = [vars[2], self.target]
            df.loc[3] = [vars[3], self.data_shape()]
            df.loc[4] = [vars[4], self.length_of_dataframe()]
            df.loc[5] = [vars[5], len(self.binary_columns())]
            df.loc[6] = [vars[6], len(self.Ternary_columns())]

            return df

        except Exception as e:
            return e

    def Nan_values(self):
        null_values_columns = [x for x in self.data.isnull().sum()]
        numeric_cols = [i for i in self.data.columns if self.data[i].isnull(
        ).sum() > 0 and self.data[i].dtypes != 'object']
        categorical_cols = [i for i in self.data.columns if self.data[i].isnull(
        ).sum() > 0 and self.data[i].dtypes == 'object']

        res = {}

        for key in list(self.data.columns):
            for value in null_values_columns:
                res[key] = value
                null_values_columns.remove(value)
                break

        remove_columns_nulls = [key for key, value in res.items() if np.float(value/self.data.shape[0]) >= 0.4]

        self.data.drop(remove_columns_nulls, axis=1, inplace=True)

        try:
            for i in remove_columns_nulls:
                if i in numeric_cols:
                    numeric_cols.remove(i)

            for i in remove_columns_nulls:
                if i in categorical_cols:
                    categorical_cols.remove(i)

            for i in numeric_cols:
                self.data[i] = self.data[i].fillna(self.data[i].mean())

            for i in categorical_cols:
                self.data[i] = self.data[i].fillna(self.data[i].mode()[0])

            self.data.dropna(inplace=True)

            return self.data

        except Exception as e:
            return("The exception caught is", e)


#estimator = Auto_Estimator(
#    "D:\\Kaggle Submision\\Titanic Dataset\\train.csv", "Survived")

#result = estimator.describe_data()

#print(result)
