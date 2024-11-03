from .Configure import Configure

config = Configure(default_config={
    "Database": {
        "DB_HOST": "",
        "DB_PORT": "",
        "DB_NAME": "",
        "DB_USER": "",
        "DB_PASS": "",
    },
    "SMTP": {
        "server": "smtp.mail.ru",
        "port": 587,
        "email": "",
        "password": ""
    },
    "OpenWeatherMap": {
        "token": "",
    },
    "Redis": {
        "host": "localhost",
        "port": 6379
    },
    "Miscellaneous": {
        "Secret": "",
        "token_expire": 3600
    }
})
