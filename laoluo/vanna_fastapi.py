

from dotenv import load_dotenv

load_dotenv()


#使用OpenAI API接口或者 OpenAI兼容本地大模型
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from fastapi import FastAPI, HTTPException, Request
from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

import pandas as pd
import asyncio
import uvicorn

from openai import OpenAI
import pandas as pd
import os
import json

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

app = FastAPI(
    title="FastAPI - JWT Authentication",
    description="EIM SWAGGER API OF JWT AUTHENTICATION WITH SQL Server. 🚀",
    version="1.0.0",
    contact={
        "name": "tietoevry",
        "email": ""
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，实际生产中可以限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQueryRequest(BaseModel):
    instruction: str

class GenerateSQLResponse(BaseModel):
    sql_sentence: str

class UserQueryResponse(BaseModel):
    answer: str

@app.post('/generate_sql', response_model=GenerateSQLResponse)
async def generate_sql(request: Request, query: UserQueryRequest):
    # auth_header = request.headers.get('Authorization')
    # if auth_header!= 'Bearer sql':
    #     raise HTTPException(status_code=403, detail="Invalid Authorization header")

    data = query.instruction
    if data is None:
        return {
            'status': 'error',
            'errorInfo': 'No instruction provided',
            'data': None
        }

    sql_sentence = vn.generate_sql(data)
    return GenerateSQLResponse(sql_sentence=sql_sentence)

    # 这里假设你有一个函数来处理SQL，比如vn.generate_sql和vn.run_sql
    # sql_result = vn.run_sql(vn.generate_sql(data))
    # return sql_result

@app.post('/query_db_by_nlp', response_model=UserQueryResponse)
async def query_db_by_nlp(request: Request, query: UserQueryRequest):
    # auth_header = request.headers.get('Authorization')
    # if auth_header!= 'Bearer sql':
    #     raise HTTPException(status_code=403, detail="Invalid Authorization header")

    data = query.instruction
    if data is None:
        return {
            'status': 'error',
            'errorInfo': 'No instruction provided',
            'data': None
        }

    sql_sentence = vn.generate_sql(data)
    # 这里假设你有一个函数来处理SQL，比如vn.generate_sql和vn.run_sql
    # sql_result = vn.run_sql(sql_sentence)

    # 将DataFrame转换为字符串
    # sql_result_str = sql_result.to_csv(sep='\t', na_rep='nan') if isinstance(sql_result, pd.DataFrame) else str(sql_result)

    sql_result = vn.run_sql(sql_sentence)

    if isinstance(sql_result, pd.DataFrame):
        sql_result = sql_result.fillna('nan')  # Fill NaN values with 'nan'
        sql_result_str = sql_result.to_json(orient='records')
    else:
        sql_result_str = json.dumps(sql_result)

    return UserQueryResponse(answer=sql_result_str)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)







