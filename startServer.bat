start rabbitmq-server

start cmd /k "cd /d E:\workspace_ptyhon\WebApp\flask_env\Scripts & activate & cd /d E:\workspace_ptyhon\WebApp & python run.py runserver

timeout 5
start cmd /k "cd /d E:\workspace_ptyhon\WebApp\flask_env\Scripts & activate  & cd /d E:\workspace_ptyhon\WebApp & celery -A apps.task.celery worker --loglevel=INFO

