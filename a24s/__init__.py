import os
from .logon import *
from .users import *
from .assignments import *
from flask import jsonify, request, Response
from werkzeug.exceptions import abort

def start(app):
    app.config.from_mapping(
        SECRET_KEY='dev',
        SECRET='nuunu'
    )

    app.config.from_pyfile('config.py', silent=True)

    def authorize():
        auth = get_user_by_access_key(request.headers['Authorization'].split()[1])
        if (not auth):
            abort(401)

    def authorize_not_student():
        auth = get_user_by_access_key(request.headers['Authorization'].split()[1])
        if (not auth) or (auth["role"] == "student"):
            abort(401)

    @app.errorhandler(401)
    def custom_401(error):
        return Response(
            'Unauthorized', 
            401
            )

    @app.route('/logon/<uuid:ukey>')
    def logon_with_user_key(ukey):
        print(ukey)
        result = get_user_by_access_key(ukey)
        return result if result else ""

    @app.route('/activate/<int:registry>')
    def activate_user_access_key(registry):
        result = create_access_key(registry)
        return {"access_key" : result} if result else ""

    @app.route('/activate/<secret>/<int:registry>')
    def activate_user_access_key_anyway(secret,registry):
        if secret == app.config["SECRET"]:
            result = create_access_key(registry, skip_check=True)
            return {"access_key" : result} if result else ""
        abort(401)

    @app.route('/users/<secret>')
    def get_all_users(secret):
        if secret == app.config["SECRET"]:
            result = exec_get_users()
            return jsonify(result)
        abort(401)

    @app.route('/assignments', methods=["GET","POST"])
    def get_assignments():
        authorize_not_student()
        if request.method == "POST":
            json = request.get_json()
            return exec_create_assignment(json)
        return jsonify(exec_get_assignments())

    @app.route('/assignments/<uuid:assignment_id>', methods=["GET","PUT","DELETE"])
    def get_assignment_by_id(assignment_id):
        if request.method == "PUT":
            authorize_not_student()
            json = request.get_json()
            return exec_update_assignment(assignment_id, json)
        if request.method == "DELETE":
            authorize_not_student()
            return exec_delete_assignment(assignment_id)
        authorize()
        return exec_get_assignment(assignment_id)

    @app.route('/assignments/<uuid:assignment_id>/activate', methods=["PUT"])
    def activate_assignment_by_id(assignment_id):
        authorize_not_student()
        return exec_activate_assignment(assignment_id)

    @app.route('/assignments/<uuid:assignment_id>/deactivate', methods=["PUT"])
    def deactivate_assignment_by_id(assignment_id):
        authorize_not_student()
        return exec_activate_assignment(assignment_id,active=False)

    @app.route('/fullfillments', methods=["GET", "POST"])
    def get_fullfillments():
        pass

    @app.route('/fullfillments/<uuid:fullfillment_id>', methods=["GET", "POST"])
    def get_fullfillments_by_id(fullfillment_id):
        pass

        
