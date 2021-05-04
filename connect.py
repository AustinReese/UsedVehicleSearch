import psycopg2
import sqlite3
import os


def connect():
    # return psycopg2.connect(host=os.environ.get("endpoint"),
    #                             user=os.environ.get("user"),
    #                             password=os.environ.get("password"),
    #                             port=os.environ.get("port"))
    return sqlite3.connect("master.db")
