from celery import Celery
from appfastapi.smtp.smtp import *
# celery -A mycelery worker -P solo -l info
# celery -A mycelery flower

app = Celery('example', broker='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True

# @app.task
# def resize_image():
#     a = 10**9
    
#     while a != 0:
#         a -= 1
    
#     return a
        
# if __name__ == "__main__":
#     resize_image.delay()