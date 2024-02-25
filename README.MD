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

#### FileBrowser Install

```
curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
```

#### Run FileBrowser

```
vim /etc/systemd/system/filebrowser.service
```

```
[Unit]
Description=FileBrowser
After=network.target

[Service]
ExecStart=filebrowser -r /root/FastApi_Celery_Redis_Flower_DrissionPage_Docker/result -a 0.0.0.0
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```
systemctl start filebrowser
systemctl status filebrowser
```
