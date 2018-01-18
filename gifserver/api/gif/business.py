import os
from PIL import Image

from gifserver.database import db
from gifserver.database.models import Gif, Tag
from gifserver import settings

def get_thumbnail_fullpath(original_path):
    base, dummy = os.path.splitext(os.path.basename(original_path))
    return os.path.join(settings.THUMBNAIL_FOLDER, base + '.png')

def create_gif(uploaded_file, filename, upload_date=None):
    gif_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    uploaded_file.save(gif_path)
                    
    im = Image.open(gif_path)
    im.seek(1)
    im.thumbnail(settings.THUMBNAIL_SIZE)
    im.convert('RGB')
    im.save(get_thumbnail_fullpath(filename), "PNG")
    
    gif = Gif(filename, upload_date)
    db.session.add(gif)
    db.session.commit()

def delete_gif(gif_id):
    gif = Gif.query.filter(Gif.id == gif_id).one()
    # remove files from filesystem
    os.remove(os.path.join(settings.UPLOAD_FOLDER, gif.name))
    os.remove(get_thumbnail_fullpath(gif.name))
    # it will also delete all associated tags
    db.session.delete(gif)
    db.session.commit()

def create_tag(gif_id, data):
    tag_value = data.get('name')
    tag = Tag.query.filter(Tag.name == tag_value).first()
    gif = Gif.query.filter(Gif.id == gif_id).one()
    if not(tag):
        tag = Tag(tag_value)
        db.session.add(tag)
    tag.gifs.append(gif)
    db.session.commit()

def delete_tag(gif_id, tag_name):
    gif = Gif.query.filter(Gif.id == gif_id).one()
    tag = Tag.query.filter(Tag.name == tag_name).one()
    gif.tags.remove(tag)
    db.session.commit()
