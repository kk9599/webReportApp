set jobname=%1
set buildid=%2

cmd /k "cd /d E:\workspace_ptyhon\WebApp\flask_env\Scripts & activate & cd /d E:\workspace_ptyhon\WebApp & python run.py Print -j="%jobname%" -b=%buildid%"