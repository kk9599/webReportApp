from apps import app
import apps.backgroundjob

BROKER_URL='amqp://guest:guest@localhost:5672//'
BACKEN_URL='amqp://guest:guest@localhost:5672//'



app.config.update(
    CELERY_BROKER_URL=BROKER_URL,
    CELERY_RESULT_BACKEND=BACKEN_URL
)

celery =  apps.backgroundjob.make_celery(app)






@celery.task()
def add(a, b):
    return a + b

@celery.task()
def importFileCelery(jobName, buildId):
    return "it works"
