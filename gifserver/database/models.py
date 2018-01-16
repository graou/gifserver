from datetime import datetime

from gifserver.database import db

association_table = db.Table('association',
    db.Column('gif_id', db.Integer, db.ForeignKey('gif.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Gif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime)

    tags = db.relationship("Tag",
                    secondary=association_table,
                    backref="gifs")

    def __init__(self, name, upload_date):
        self.name = name
        if upload_date is None:
            upload_date = datetime.utcnow()
        self.upload_date = upload_date

    def __repr__(self):
        return '<Gif %r>' % self.name

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
