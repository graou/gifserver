from flask_restplus import fields
from gifserver.api.restplus import api

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

tag = api.model('Tag', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a tag'),
    'name' : fields.String(required=True, description='Tag value'),
})

gif = api.model('Gif', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a gif'),
    'name': fields.String(required=True, description='Filename of the gif'),
    'upload_date': fields.DateTime,
    'tags': fields.List(fields.Nested(tag)),
})

page_of_gifs = api.inherit('Page of gifs', pagination, {
    'items': fields.List(fields.Nested(gif))
})