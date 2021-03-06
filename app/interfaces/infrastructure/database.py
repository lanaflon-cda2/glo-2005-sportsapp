import pymysql.cursors

from app import app
from app.interfaces.database import Database


class MySQLDatabase(Database):
    def create_connection(self):
        return pymysql.connect(host=app.config['MYSQL_HOST'],
                               user=app.config['MYSQL_USER'],
                               password=app.config['MYSQL_PASSWORD'],
                               db=app.config['MYSQL_DB'],
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
