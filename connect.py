import psycopg2
import sqlite3
import os


def connect(offline_debug):
    if offline_debug == False:
        conn = psycopg2.connect(host=os.environ.get("endpoint"),
                                user=os.environ.get("user"),
                                password=os.environ.get("password"),
                                port=os.environ.get("port"))
    else:
        return sqlite3.connect("data/vehicles.db")
    return conn
