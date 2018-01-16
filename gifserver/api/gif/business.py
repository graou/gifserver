import os
from PIL import Image

from gifserver.database import db
from gifserver.database.models import Gif
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
    db.session.delete(gif)
    # TODO delete all associated tags
    db.session.commit()
