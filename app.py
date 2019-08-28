# encoding=utf-8

from flask import Flask
import logging
import logging.handlers

import views

BLUEPRINTS = [
    (views.website, '')
]

LOGGERS = {}


def create_log(name):
    global LOGGERS

    if "name" in LOGGERS.keys():
        return LOGGERS["name"]

    logging.getLogger('tornado.access').disabled = True
    logging.getLogger('bmemcached.protocol').disabled = True
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)

    new_log = logging.getLogger(name)

    app_formatter = logging.Formatter(
        "%(asctime)s\t%(process)d|%(thread)d\t%(module)s | %(funcName)s | %(filename)s:%(lineno)d"
        "\t%(levelname)s\t%(message)s", "%Y-%m-%d@%H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(app_formatter)
    console_handler.setLevel(logging.DEBUG)

    new_log.propagate = False
    new_log.addHandler(console_handler)
    new_log.setLevel(logging.DEBUG)

    LOGGERS.update(dict(name=new_log))
    return new_log


def create_app():
    app = Flask(__name__)
    blueprints = BLUEPRINTS
    for view, url_prefix in blueprints:
        app.register_blueprint(view, url_prefix=url_prefix)
    app.my_logger = create_log('web')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9500, debug=True)
