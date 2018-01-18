# gifserver

A simple server providing a REST API to upload/retrieve/tag/search gifs.

## starting the server

```bash
pip install -r requirements.txt
python gifserver/app.py
```
## configuration

See setting.py.
The server will listen on port 8888 by default.
`UPLOAD_FOLDER` and `THUMBNAIL_FOLDER` should be set to valid directories.

## API

All the available API endpoints can listed by opening the following URL in your favorite brower `http://localhost:8888/api/`

