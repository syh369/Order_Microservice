import os
# This is a bad place for this import
import pymysql


class Context:
    def __init__(self):
        pass

    @staticmethod
    def get_db_info():
        """
        :return: A dictionary with connect info for MySQL
        """
        h = os.environ.get("DBHOST", None)
        usr = os.environ.get("DBUSER", None)
        pw = os.environ.get("DBPW", None)

        if h is not None:
            db_info = {
                "host": h,
                "user": usr,
                "password": pw,
                "cursorclass": pymysql.cursors.DictCursor,
                # auto commit
            }
        else:
            # If no environment variables set go local
            db_info = {
                "host": "localhost",
                "user": "root",
                "password": "dbuserbdbuser", # OR use dbuserdbuser.
                "cursorclass": pymysql.cursors.DictCursor
            }

        return db_info
