import logging

from flask import request
from flask_restplus import Resource
from gifserver.api.gif.business import create_gif, delete_gif, create_tag, delete_tag
from gifserver.api.gif.serializers import page_of_gifs, gif, tag, tags
from gifserver.api.gif.parsers import pagination_arguments, upload_parser
from gifserver.api.restplus import api
from gifserver.database.models import Gif, Tag
from werkzeug.utils import secure_filename
from gifserver import settings

log = logging.getLogger(__name__)

ns = api.namespace('gifs', description='Operations related to gifs')

@ns.route('/')
class GifCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_gifs)
    def get(self):
        """
        Returns list of gifs.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        gifs_query = Gif.query
        gifs_page = gifs_query.paginate(page, per_page, error_out=False)

        return gifs_page

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        for uploaded_file in args['file']:
            try:
                if self.allowed_file(uploaded_file.filename):
                    filename = secure_filename(uploaded_file.filename)
                    create_gif(uploaded_file, filename)
            except Exception as e:
                log.error(e)
        return None, 201
 
 
@ns.route('/<int:id>')
@api.response(404, 'Gif not found.')
class GifItem(Resource):

    @api.marshal_with(gif)
    def get(self, id):
        """
        Returns a gif.
        """
        return Gif.query.filter(Gif.id == id).one()

    @api.response(204, 'Gif successfully deleted.')
    def delete(self, id):
        """
        Deletes a gif.
        """
        delete_gif(id)
        return None, 204


@ns.route('/<int:gif_id>/tags')
@api.response(404, 'Gif not found.')
class TagCollection(Resource):

    @api.marshal_list_with(tag)
    def get(self, gif_id):
        """
        Returns the list of tags associated to a gif.
        """
        return Tag.query.filter(Tag.gifs.any(id=gif_id)).all()

    @api.response(201, 'Tag successfully created.')
    @api.expect(tag)
    def post(self, gif_id):
        """
        Adds a tag to a gif.
        """
        data = request.json
        create_tag(gif_id, data)
        return None, 201


@ns.route('/<int:gif_id>/tags/<string:tag_name>')
@api.response(404, 'Tag not found.')
class TagItem(Resource):
    
    @api.response(204, 'Tag successfully deleted.')
    def delete(self, gif_id, tag_name):
        """
        Removes a tag from a gif.
        """
        delete_tag(gif_id, tag_name)
        return None, 204