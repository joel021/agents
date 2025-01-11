import os
from mongoengine import connect
from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, WORK_DIR
from agents.flask_app import *


def main():

    connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT),
            authentication_source='admin')

    os.makedirs(WORK_DIR, exist_ok=True)


if __name__ == "__main__":

    main()
    app.run("127.0.0.1", port=8080, debug=True)
