from matplotlib import pyplot
from scipy import stats
from scipy.stats import normaltest
from sqlalchemy import create_engine
from sqlalchemy import inspect
from statsmodels.graphics.gofplots import qqplot

import pandas as pd
import seaborn as sns
import yaml

###

class DataFrameInfo:
    """
        Class containing functions which takes in a dataframe as input and performs various statistitcal enquiries on it.
    """
    
    def show_info(self,dataframe):
        """
            Applies .info() to dataframe
        """
        dataframe.info()

    def return_all_columns(self,dataframe):
        """
            Returns an array of all but the first two column names. We skip the first two as to avoid the index and id columns.
        """
        return dataframe.columns[2:]
    
    def show_statistical_values(self, list_of_columns:list):
        """ 
            Iterates over all but the first two columns to give statistical values. Checks the dtype first and shows an appropriate set of statistics based on dtype. 
        """
        for column in list_of_columns:
            print(f"\nStatistical values for {column.name}:")
            if column.dtype in ['int64', 'float64']:
                print(f"Mean:{column.mean()}")
                print(f"Median:{column.median()}")
                print(f"Mode:{column.mode()}")
                print(f"Standard deviation: {column.std()}")
                print(f"Skew: {column.skew()}")
            if column.dtype in ['bool', 'object']:
                print(f"Mode:{column.mode()}\n")

    def show_shape(self,dataframe):
        """
            Prints the shape of the dataframe.
        """
        print(f"The dataframe has shape {dataframe.shape}")

    def percentage_of_non_null_values(self,dataframe_series):
        """
            Takes in a column name as a string and returns the percentage of non-null values within it.
        """
        num_of_non_null_values = dataframe_series.count()
        num_of_null_values = dataframe_series.isnull().sum()
        percentage_of_non_null_values = (num_of_non_null_values / (num_of_non_null_values + num_of_null_values)) * 100
        #print(num_of_null_values)
        return percentage_of_non_null_values
    
    def null_value_information(self,dataframe_series):
        print(f"\nNull value information for {dataframe_series.name}: \nPercentage of non-null values: {self.percentage_of_non_null_values(dataframe_series)} %")
        if dataframe_series.dtype in ['int64', 'float64']:
            print(normaltest(dataframe_series, nan_policy = 'omit'))


###

class DataTransform:
    """
        Class containing functions which performs extracting/cleaning/transforming/tasks
    """
    def map_0_1_to_boolean(self, number:int):
        """
            Takes in an integer as input. Maps 0 to False and 1 to True, leaves all other number as they are.
        """
        if number == 0: return False
        elif number == 1: return True
        else: return number

    def boolean_convert(self, dataframe_input, column):
        """
            Applies map_0_1_to_boolean to an to a column in dataframe_input.
        """
        df = dataframe_input
        df[column] = df[column].map(self.map_0_1_to_boolean)
        return df

    def map_strings_to_ordinals(self, string:str, key_of_strings:list):
        try:
            return key_of_strings.index(string)
        except ValueError:
            return -1
    
    def string_convert(self, dataframe, column, key_of_strings):
        return dataframe[column].map(lambda x : self.map_strings_to_ordinals(x, key_of_strings))
    
    def read_db_creds(self, file_path):
        """
            Open a YAML file, then print and return the contents.
        """
        with open(file_path, 'r') as imported_file:
            #print(yaml.safe_load(imported_file))
            return yaml.safe_load(imported_file)
        
    def read_csv_as_dataframe(self, file_path):
        """
            Reads a .csv file with directory 'file_path' and returns a pandas dataframe
        """
        with open(file_path, 'r') as imported_file:
            return pd.read_csv(imported_file)
    

###

class RDSDatabaseConnector:
    """
        Creates an sqlalchemy engine to from a dictionary of credentials and performs various actions with the engine.
    """

    def __init__(self, dictionary_of_credentials:dict):
        """
            Sets up the connection to the engine via credentials in dictionary_of_credentials 
        """
        self.dictionary_of_credentials = dictionary_of_credentials
    
    def init_db_engine(self):
        """
            Returns an sqlalchemy via the credentials in self.dictionary_of_credentials.
        """
        dictionary_of_credentials = self.dictionary_of_credentials
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = dictionary_of_credentials['RDS_HOST']
        USER = dictionary_of_credentials['RDS_USER']
        PASSWORD = dictionary_of_credentials['RDS_PASSWORD']
        DATABASE = dictionary_of_credentials['RDS_DATABASE']
        PORT = dictionary_of_credentials['RDS_PORT']
        #print(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        return create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    
    def list_db_tables(self):
        """
            Passes init_db_engine and list the tables in the connected database
        """
        engine = self.init_db_engine()
        engine.execution_options(isolation_level='AUTOCOMMIT').connect()
        inspector = inspect(engine)
        print(inspector.get_table_names())
    
    def read_rds_table(self, table_name:str):
        """
            Returns a pandas dataframe with name 'table_name' from self.init_db_engine()
        """
        return pd.read_sql_table(table_name, self.init_db_engine())
    
    def rds_table_to_csv(self, table_name:str, file_name:str = 'csv_of_dataframe.csv'):
        """
            Puts the resulting dataframe from 'read_rds_table' in a .csv file
        """
        pd.read_sql_table(table_name, self.init_db_engine()).to_csv(file_name)

###

class Plotter:
    """
    
    """
    def show_correlation_plot(self, dataframe):
        sns.heatmap(dataframe.corr(numeric_only=True), cmap='coolwarm')
    
    def show_histogram(self, dataframe_series, bin_number=20):
        dataframe_series.hist(bins=bin_number)
    
    def show_box_plot(self, dataframe_series):
        sns.boxplot(y=dataframe_series, color='lightgreen', showfliers=True)
        #sns.swarmplot(y=dataframe_series, color='black')
    
    def show_qq_plot(self, dataframe_series):
        pass

    def show_scatter_plot(self, series_1, series_2):
        sns.scatterplot(x = series_1, y = series_2)


###

class DataFrameTransform:
    """

    """
    
    def impute_median(self, dataframe_series):
        return dataframe_series.fillna(dataframe_series.median())
    
    def apply_box_cox(self, dataframe_series):
        return pd.Series(stats.boxcox(dataframe_series)[0])