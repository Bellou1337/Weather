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
    "TOKEN": {
        "key": "",
    }

})
