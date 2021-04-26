import os
import werkzeug
from flask import request

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev",)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def catch_badrequest(u_path):
        result = "Bad, bad, bad, very bad", 400
        app.logger.warning(result[0])
        return result 

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def catch_notfound(u_path):
        result = "Not found", 404
        app.logger.info(result[0])
        return result

    @app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
    def catch_methodnotallowed(u_path):
        result = "Method Not Allowed", 405
        app.logger.info(result[0])
        return result

    @app.route('/api', defaults={'u_path': 'list'})
    @app.route('/api/<path:u_path>')
    def catch_api(u_path):
        result = "lolkek", 200
        req_args = request.args

        print('path is {}'.format(u_path))

        if u_path == 'list':
            result = api_list()
        elif u_path == 'create':
            result = api_create()
        elif u_path == 'delete':
            result = api_delete(req_args)
        elif u_path == 'read':
            result = api_read()
        else:
            result = api_not_implemented()

        if req_args.get('invalid') == '1':
            result = "invalid", 400

        if result[1] != 200:
            app.logger.warning(result[0])
        else:
            app.logger.info(result[0])

        return result

    def api_list():
        return "list", 200

    def api_create():
        return "created", 200

    def api_delete(req_args):
        if req_args.get('notawaiting') == '1':
            return "notawaiting", 400
        return "deleted", 200
    
    def api_read():
        return "readed", 200

    def api_not_implemented():
        return "Not implemented", 501

    return app
