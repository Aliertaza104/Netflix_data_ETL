import psycopg2

class DBConnection:

    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.config.DB_NAME,
            user=self.config.USER,
            password=self.config.PASSWORD,
            host=self.config.HOST,
            port=self.config.PORT
        )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
