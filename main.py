#!/usr/bin/env python3
import os
import logging
from flask import has_request_context, request
from flask.logging import default_handler

from webtrap import create_app

if __name__ == '__main__':
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.method = request.method
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None

            return super().format(record)


    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s by method %(method)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)

    app = create_app()
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port)
