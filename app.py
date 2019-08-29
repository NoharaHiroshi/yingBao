# encoding=utf-8

from flask import Flask
import logging
import logging.handlers

import views

BLUEPRINTS = [
    (views.website, '')
]


def create_app():
    app = Flask(__name__)
    blueprints = BLUEPRINTS
    for view, url_prefix in blueprints:
        app.register_blueprint(view, url_prefix=url_prefix)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9500, debug=True)
