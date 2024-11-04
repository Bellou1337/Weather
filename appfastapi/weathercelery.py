import time
import asyncio
from appfastapi.config import config
from appfastapi.openweathermap.api import weather_the_future
from celery import Celery, shared_task
from appfastapi.schemas.schemas import WeatherRequest
from datetime import datetime, timedelta
from appfastapi.database.redis import RedisTools
# celery -A appfastapi.weathercelery worker -P solo -l info
# celery -A appfastapi.weathercelery beat -l info

app = Celery('weathercelery',
             broker=f"redis://{config['Redis']['host']}:{config['Redis']['port']}/0")
app.conf.broker_connection_retry_on_startup = True

app.conf.update(
    timezone="UTC",
    beat_schedule={
        "fetch-weather-every-24-hours": {
            "task": "appfastapi.weathercelery.fetch_and_store_weather_data",
            "schedule": 86400,
        }
    }
)


@shared_task
def fetch_and_store_weather_data():

    cities = RedisTools.get_city_list()
    if len(cities) == 0:
        print("weathercelery list is empty")
        return

    for city in cities:

        city_name = city.decode("utf-8")
        request_data = WeatherRequest(
            city_name=city_name,
            date_time=get_previous_3_hour_mark(datetime.utcnow())
        )
        try:
            asyncio.run(weather_the_future(request_data))

        except Exception as e:
            print("weathercelery failed", e)
        finally:
            time.sleep(1)


def get_previous_3_hour_mark(dt):

    dt += timedelta(hours=3)
    dt = dt.replace(minute=0, second=0, microsecond=0)
    remainder = dt.hour % 3
    dt -= timedelta(hours=remainder)
    return dt
