import os
from .logon import get_user_by_access_key, create_access_key
from werkzeug.exceptions import abort

def start(app):
    app.config.from_mapping(
        SECRET_KEY='dev',
        SECRET='nuunu'
    )

    app.config.from_pyfile('config.py', silent=True)

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
        raise(400)
