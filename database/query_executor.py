import pandas as pd
from tqdm import tqdm
import logging
import os

class QueryExecutor:

    def __init__(self, connection, results_dir="results"):
        self.conn = connection
        self.results_dir = results_dir

        # Setup logging
        logging.basicConfig(
            filename="query_execution.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Create results directory if not exists
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def run_query(self, sql_query, params=None):
        """
        Execute a single SQL query and return results as a Pandas DataFrame
        """
        try:
            df = pd.read_sql_query(sql_query, self.conn, params=params)
            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            print(f"Error executing query: {e}")
            return pd.DataFrame()

    def run_insert_query(self, sql_query, params=None):
        """
        Execute an INSERT/UPDATE/DELETE query
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query, params)
            self.conn.commit()
            cursor.close()
            logging.info(f"Insert/Update executed successfully: {sql_query}")
        except Exception as e:
            logging.error(f"Error executing insert/update: {e}")
            print(f"Error executing insert/update: {e}")

    def run_multiple_queries(self, queries: dict):
        """
        Run multiple queries stored as {query_name: query_sql} and return results in dict
        """
        results = {}
        for name, query in tqdm(queries.items(), desc="Executing Queries"):
            logging.info(f"Executing query: {name}")
            df = self.run_query(query)
            results[name] = df
            if not df.empty:
                print(f"\nTop 5 rows for {name}:")
                print(df.head())
        return results

    def save_results(self, results: dict):
        """
        Save all DataFrames in results dict to CSV
        """
        for name, df in results.items():
            path = os.path.join(self.results_dir, f"{name}.csv")
            df.to_csv(path, index=False)
            logging.info(f"Saved CSV: {path}")
            print(f"Saved CSV: {path}")
