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
    -v /path/to/root:/srv \
    -v /path/to/filebrowser.db:/database/filebrowser.db \
    -v /path/to/settings.json:/config/settings.json \
    -e PUID=$(id -u) \
    -e PGID=$(id -g) \
    -p 8080:80 \
    filebrowser/filebrowser:s6
```
