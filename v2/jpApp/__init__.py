import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'jpApp.sqlite')
    )

    #we assume test_config will be None for now.

    app.config.from_pyfile('config.py', silent=True)

    #ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello.
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    from . import revision
    app.register_blueprint(revision.bp)

    from . import study
    app.register_blueprint(study.bp)
    

    return app
