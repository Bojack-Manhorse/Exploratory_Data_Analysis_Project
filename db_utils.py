from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import yaml

def read_db_creds(file_path):
        """
            Open a YAML file, then print and return the contents.
        """
        with open(file_path, 'r') as imported_file:
            #print(yaml.safe_load(imported_file))
            return yaml.safe_load(imported_file)

def read_csv_as_dataframe(file_path):
    """
        Reads a .csv file with directory 'file_path' and returns a pandas dataframe
    """
    with open(file_path, 'r') as imported_file:
        return pd.read_csv(imported_file)

class RDSDatabaseConnector:
    """
        Connect and upload data to the database.
    """

    def __init__(self, dictionary_of_credentials:dict):
        self.dictionary_of_credentials = dictionary_of_credentials
    
    def init_db_engine(self):
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
            Puts the resulting datafeame from 'read_rds_table' in a .csv file
        """
        pd.read_sql_table(table_name, self.init_db_engine()).to_csv(file_name)


