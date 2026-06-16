import sqlite3
import pandas as pd

def get_prediction_history():

    conn = sqlite3.connect("healthcare.db")

    query = """
    SELECT
        id,
        disease,
        confidence,
        created_at
    FROM predictions
    ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df