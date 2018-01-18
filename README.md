# gifserver

**This is still an ugly WIP project**

A simple server providing a REST API to upload/retrieve/tag/search gifs.

## starting the server

```bash
pip install -r requirements.txt
python gifserver/app.py
```
## configuration

See gifserver/setting.py.

The server will listen on port 8888 by default.

`UPLOAD_FOLDER` and `THUMBNAIL_FOLDER` should be set to valid directories.

## API

All the available API endpoints can listed and tested by opening the following URL in your favorite browser `http://localhost:8888/api/`

A test upload form is available in `examples/upload.html`

Note that uploading a gif will store it in `UPLOAD_FOLDER` and generate a static thumbnail in `THUMBNAIL_FOLDER`.

All the gif metadata and tags are stored in a sqlite database.
