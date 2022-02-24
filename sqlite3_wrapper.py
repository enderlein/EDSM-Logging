import sqlite3

def create_table(db_filename, table_name, columns):
    # columns (list) - 
    connection = sqlite3.connect(db_filename)
    cur = connection.cursor()

    table_exists = cur.execute("SELECT name FROM sqlite_naster WHERE type = \'table\' AND name NOT LIKE \'sqlite_%\';")
    if not table_exists:
        col = columns ## TODO format columns list
        cur.execute(f"CREATE TABLE {table_name} {columns}")

    else:
        raise Exception(f"Table {table_name} already exists in {db_filename}")

def insert_into(db_filename, table_name, values):
    # DICT - vals - key-value pairs to be inserted into table
    ##################
    connection = sqlite3.connect(db_filename)
    cur = connection.cursor()

    keys = ', '.join(list(values.keys())) # TODO use list comprehensions
    vals = ', '.join(list(values.values())) # TODO format vals so they are contained in quotes within string (where needed)

    cur.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({vals});")

# add sql_wrapper function for searching database