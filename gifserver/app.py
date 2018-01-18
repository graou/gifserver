import logging.config

import sys
import os
sys.path.append(os.getcwd())

from flask import Flask, Blueprint
from gifserver import settings
from gifserver.api.gif.endpoints.gifs import ns as gifs_namespace
from gifserver.api.gif.endpoints.tags import ns as tags_namespace
from gifserver.api.restplus import api
from gifserver.database import db
from gifserver.database import reset_database

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
    flask_app.config['ALLOWED_EXTENSIONS'] = settings.ALLOWED_EXTENSIONS
    flask_app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(gifs_namespace)
    api.add_namespace(tags_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
