##### FastApi_Celery_Redis_Flower_DrissionPage_Docker

#### FastApi

```
cd app
uvicorn main:app --reload
```

#### Celery

```
celery -A tasks worker --concurrency=1 --loglevel=info
celery -A tasks flower --port=5555
```

#### Docker Build

docker compose -f docker-compose.yml up -d --build

#### FileBrowser

```
docker run \
    -v /root/FastApi_Celery_Redis_Flower_DrissionPage_Docker/result:/srv \
    -v /root/filebrowser/filebrowser.db:/database/filebrowser.db \
    -v /root/filebrowser/settings.json:/config/settings.json \
    -e PUID=$(id -u) \
    -e PGID=$(id -g) \
    -p 5060:80 \
    filebrowser/filebrowser:s6
```
