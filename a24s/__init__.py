import os

def start(app):
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.config.from_pyfile('config.py', silent=True)

    # a simple page that says hello
    @app.route('/logon/<ukey>')
    def logon_with_user_key(ukey):
        if ukey == '01d06ad4-a0ea-46fb-8029-bf9d9a3efc60':
            return {
                "name": "test",
                "key" : ukey
            }
        return f"<p>Key is {ukey} and is {ukey == '01d06ad4-a0ea-46fb-8029-bf9d9a3efc60'}</p>"
