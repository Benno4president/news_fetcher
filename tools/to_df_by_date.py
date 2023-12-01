import sys
sys.path.insert(0,'.')
from app.datahandler import ToolDBInterface
from pandas import DataFrame
import datetime

list_of_res = ToolDBInterface().get_all_sorted_by_date()

df:DataFrame = DataFrame([dict(x) for x in list_of_res])
df.drop('_sa_instance_state', inplace=True, axis=1)
df.text = df.text.apply(lambda x : x.replace('\n', ''))
df.to_csv(f'db_dump_len{len(df)}.csv', escapechar='\\', index=None)