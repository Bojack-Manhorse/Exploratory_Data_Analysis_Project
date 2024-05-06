from db_utils import DataFrameInfo
from db_utils import DataFrameTransform
from db_utils import DataTransform
from db_utils import RDSDatabaseConnector

my_transformer = DataTransform()
my_extractor = RDSDatabaseConnector(my_transformer.read_db_creds("db_creds.yaml"))

#my_extractor.rds_table_to_csv('failure_data')

df = my_transformer.read_csv_as_dataframe('csv_of_dataframe.csv')
my_frame_info = DataFrameInfo()
my_dataframe_transformer = DataFrameTransform()

df.info()

def transform_data(dataframe, list_of_columns):
    for column_name in list_of_columns: #['Machine failure', 'TWF','HDF','PWF','OSF','RNF']:
        dataframe = my_transformer.boolean_convert(dataframe, column_name)

def show_null_information(dataframe, list_of_columns): 
    for column in list_of_columns:
        #print(column)
        my_frame_info.null_value_information(dataframe, column)

#show_null_information(df,df.columns.values[2:])

### The three rows with missing values (Air temperature [K],Process temperature [K] and Tool wear [min] ) all have low p-values, so we'll impute with median

def impute_median_of_all_columns(dataframe, list_of_columns):
    for column in list_of_columns:
        dataframe[column] = my_dataframe_transformer.impute_median(dataframe[column])

impute_median_of_all_columns(df, ['Air temperature [K]','Process temperature [K]', 'Tool wear [min]'])

#show_null_information(df, ['Air temperature [K]','Process temperature [K]', 'Tool wear [min]'])