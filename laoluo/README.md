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

## Run the server
```
python app.py

docker compose build
docker compose up
```

