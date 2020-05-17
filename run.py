# run.py

import os

from app import create_app

app = create_app(os.getenv('FLASK_RUNNING_MOD','development'))


if __name__ == '__main__':
    app.run()