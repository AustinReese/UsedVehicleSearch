import psycopg2


def fetchCreds():
    f = open("creds/creds.txt")
    creds = {}
    for line in f.readlines():
        creds[line.split("|")[0]] = line.split("|")[1].strip()
    return creds

def connect():
    #fetch credentials
    creds = fetchCreds()
    #connect to database
    conn = psycopg2.connect(host = creds["endpoint"],
                            user = creds["user"],
                            password = creds["password"],
                            database = "postgres",
                            port = creds["port"])
    return conn