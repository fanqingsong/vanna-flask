# vanna-flask
Web server for chatting with your database

https://mp.weixin.qq.com/s/KzuwZNjYL5-IjcybHLETfQ
https://zhuanlan.zhihu.com/p/690193634
https://vanna.ai/docs/mssql-openai-standard-chromadb/


# Setup

## Set your environment variables
```
```

## Install dependencies

```
# pydoc 依赖
sudo apt-get update
sudo apt-get install unixodbc-dev

# driver
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
ACCEPT_EULA=Y sudo apt-get install -y msodbcsql17


python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Run Dev server
```
uv venv
source .venv/bin/activate

uv venv --python 3.10.12
source .venv/bin/activate

pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

export UV_HTTP_TIMEOUT=60
uv pip install -r requirements.txt

python vanna_fastapi.py
or
uvicorn vanna_fastapi:app --reload --port 5001
```


## Deploy the server
```
docker exec -it laoluo-myvanna-flask-app-1 bash python3 -V

Python 3.10.12
 
docker compose build
docker compose up

docker logs -f laoluo-myvanna-fastapi-app-1
docker logs -f laoluo-myvanna-flask-app-1
```

