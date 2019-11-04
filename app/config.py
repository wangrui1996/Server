import os
project_root = os.getcwd()
SECRET_KEY = 'hard to guess string'
UPLOAD_FOLDER = os.path.join(project_root, 'app/uploads')
THUMBNAIL_FOLDER = os.path.join(project_root, 'app/uploads/thumbnail')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 50 # 16 * 50 MB