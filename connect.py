import psycopg2
import os

def connect():
    conn = psycopg2.connect(host = os.environ.get("endpoint"),
                            user = os.environ.get("user"),
                            password = os.environ.get("password"),
                            database = os.environ.get("database"),
                            port = os.environ.get("port"))
    return conn