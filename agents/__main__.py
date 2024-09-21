from mongoengine import connect

from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def main():
    db_connection_string = (f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    connect(db_connection_string)



if __name__ == "__main__":

    main()

