import psycopg2
from .config import config


def check_connect():
    conn = None
    params = config()
    # print(params)
    try:
        params = config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()  # to execute psql commands..

        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        print("PostgreSQL database version: ", db_version)

        cur.close()

        # conn.commit()  for inserting data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  # very important to close the connection
            print("Database connection closed.")


def fetchall():
    """insert a new vendor into the vendors table"""
    commands = """SELECT * FROM products"""
    conn = None
    data = []
    output = {}
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(commands)

        row = cur.fetchone()

        while row is not None:
            data.append(row)
            row = cur.fetchone()
        for i in data:
            res = {}
            res["name"] = i[1]
            res["des"] = i[2]
            res["price"] = i[3]
            res["tax"] = i[4]
            output[f"id={i[0]}"] = res
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return output


def create_tables():
    """insert a new vendor into the vendors table"""
    commands = (
        """
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            des TEXT NULL,
            price VARCHAR(10),
            tax VARCHAR(3)
        )
        """,
    )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_data(name, des, price, tax):
    """insert a new vendor into the vendors table"""

    sql = """INSERT INTO products(name, des, price, tax)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    conn = None
    id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (name, des, price, tax))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return id


if __name__ == "__main__":
    x = fetchall()
    print(x)
