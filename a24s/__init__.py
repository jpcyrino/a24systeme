import os
from .logon import *
from .users import *
from .assignments import *
from .fullfillments import *
from .reviews import *
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

    @app.route('/users', methods=["GET","POST"])
    def get_users():
        if request.method=="POST":
            json = request.get_json()
            return exec_insert_user(json)
        return jsonify(exec_get_users())

    @app.route('/assignments', methods=["GET","POST"])
    def get_assignments():
        if request.method == "POST":
            authorize_not_student()
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
        authorize()
        if request.method == "POST":
            json = request.get_json()
            return exec_create_fullfillment(json)
        return jsonify(exec_get_fullfillments())

    @app.route('/fullfillments/<uuid:fullfillment_id>', methods=["GET", "PUT", "DELETE"])
    def get_fullfillments_by_id(fullfillment_id):
        if request.method == "DELETE":
            authorize_not_student()
            return exec_delete_fullfillment(fullfillment_id)
        authorize()
        if request.method == "PUT":
            json = request.get_json()
            return exec_update_fullfillment(fullfillment_id,json)
        return exec_get_fullfillment(fullfillment_id)
    
    @app.route('/fullfillments/user/<uuid:user_id>')
    def get_fullfillments_by_user_id(user_id):
        return jsonify(exec_get_fullfillments_by_user_id(user_id))

    @app.route('/reviews')
    def get_reviews():
        authorize_not_student()
        return jsonify(exec_get_reviews())

    @app.route('/reviews/<uuid:review_id>', methods=["GET", "PUT", "DELETE"])
    def get_reviews_by_id(review_id):
        if request.method=="GET":
            authorize()
            return exec_get_review(review_id)
        authorize_not_student()
        if request.method=="DELETE":
            return exec_delete_review(review_id)
        json = request.get_json()
        return exec_update_review(review_id, json)

    @app.route('/reviews/reviewer/<uuid:user_id>')
    def get_reviews_by_reviewer_id(user_id):
        authorize_not_student()
        return jsonify(exec_get_reviews_by_reviewer_id(user_id))

    @app.route('/reviews/fullfillment/<uuid:fullfillment_id>')
    def get_review_by_fullfillment_id(fullfillment_id):
        authorize()
        return exec_get_review_by_fullfillment_id(fullfillment_id)
        
    @app.route('/reviews/send/<uuid:review_id>', methods=["PUT"])
    def send_review(review_id):
        authorize_not_student()
        return exec_send_review(review_id)