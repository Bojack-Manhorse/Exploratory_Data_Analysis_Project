from db_utils import RDSDatabaseConnector
from db_utils import read_db_creds
from db_utils import read_csv_as_dataframe

my_extractor = RDSDatabaseConnector(read_db_creds("db_creds.yaml"))

#my_extractor.rds_table_to_csv('failure_data')

print(read_csv_as_dataframe('csv_of_dataframe.csv'))