from constants.shared_consts import APPLICATION_ROOT

test_config = {
    "version": 1,
    "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": f"{APPLICATION_ROOT}/logger/files/test.log",
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s:%(message)s",
            "datefmt": "%m-%d-%Y %I:%M:%S",
        }
    },
}

dev_config = {
    "version": 1,
    "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": f"{APPLICATION_ROOT}/logger/files/dev.log",
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s:%(message)s",
            "datefmt": "%m-%d-%Y %I:%M:%S",
        }
    },
}

prod_config = {
    "version": 1,
    "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": f"{APPLICATION_ROOT}/logger/files/app.log",
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s:%(message)s",
            "datefmt": "%m-%d-%Y %I:%M:%S",
        }
    },
}
