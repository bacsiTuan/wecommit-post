# redis pubsub
## install required packages
activate virtual env (optional)
```bash
#macos
#create if not exists
python -m venv venv
source venv/bin/activate
```
run redis with docker
```bash
docker compose up -d redis
```
install dependencies
```bash
cd redis-pubsub
pip install -r requirements.txt
```

## run command
```bash
python rd_sub.py
python rd_pub.py
