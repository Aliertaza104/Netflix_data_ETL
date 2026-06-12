class SchemaManager:

    def __init__(self, connection, schema_path):
        self.connection = connection
        self.schema_path = schema_path

    def create_schema(self):
        cursor = self.connection.cursor()

        with open(self.schema_path, "r") as file:
            sql_script = file.read()

        cursor.execute(sql_script)
        self.connection.commit()
        cursor.close()
