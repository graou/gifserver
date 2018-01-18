import logging

from flask import request
from flask_restplus import Resource
from gifserver.api.gif.serializers import page_of_gifs, gif, tag, tags, page_of_tags
from gifserver.api.gif.parsers import pagination_arguments
from gifserver.api.restplus import api
from gifserver.database.models import Gif, Tag
from gifserver import settings

log = logging.getLogger(__name__)

ns = api.namespace('tags', description='Operations related to tags')

@ns.route('/')
class TagCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_tags)
    def get(self):
        """
        Returns the list of tags defined.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        # TODO handle no results
        return Tag.query.paginate(page, per_page, error_out=False)


@ns.route('/<string:tag_name>')
class TagItem(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_gifs)
    def get(self, tag_name):
        """
        Returns list of gifs associated to given tag.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        gifs_page = Gif.query.filter(Gif.tags.any(Tag.name == tag_name)).paginate(page, per_page, error_out=False)
        return gifs_page
