#使用OpenAI API接口或者 OpenAI兼容本地大模型
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from openai import OpenAI
import pandas as pd
import os

# client = OpenAI(
#     api_key="OpenAI Key或者OpenAI代理Key",
#     base_url="OpenAI URL或者OpenAI代理URL",
# )
#OneAPI包装本地LLM后外露的OpenAI兼容接口
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


# vn = MyVanna(client=client, config={"model": "gpt-3.5-turbo"})
# 接入OpenAI兼容本地大模型
# vn = MyVanna(client=client, config={"model": "moonshot-v1-8k"})
vn = MyVanna(client=client, config={"model": os.getenv("OPENAI_API_MODEL")})

# vn.connect_to_mysql(host='192.168.0.13', dbname='test', user='test', password='123456', port=3306)

# 配置连接参数
driver = '{ODBC Driver 17 for SQL Server}'
server =  os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")
# port = 1433

# 使用模板字符串生成连接字符串
odbc_conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# 调用连接方法
vn.connect_to_mssql(odbc_conn_str=odbc_conn_str)

#读取列数据让训练
# The information schema query may need some tweaking depending on your database. This is a good starting point.
df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

# This will break up the information schema into bite-sized chunks that can be referenced by the LLM
plan = vn.get_training_plan_generic(df_information_schema)

# If you like the plan, then uncomment this and run it to train
vn.train(plan=plan)


from vanna.flask import VannaFlaskApp
VannaFlaskApp(
    vn,
    debug=True,
    allow_llm_to_see_data=True,
    show_training_data=True,
).run(host='0.0.0.0',port=5000)





