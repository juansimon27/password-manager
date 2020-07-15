import os
from sqlite3 import connect, OperationalError
from time import ctime


DATABASE = "credentials.db"
MASTER_PASSWORD = "Juanita"


def authentication(func):
    def wrapper():
        initial_input = input("Insert password to access credentials:\n")

        while initial_input != MASTER_PASSWORD:
            print("Incorrect Password -> DENIED ACCESS\n")
            initial_input = input("Insert password to access credentials:\n")

            if initial_input == "quit":
                break

        if initial_input == MASTER_PASSWORD:
            print("Correct Password -> ACCESS GRANTED")
            return func()

    return wrapper


def create_table(c):
    sql_command = '''
                        CREATE TABLE IF NOT EXISTS credentials_table(
                            website TEXT PRIMARY KEY,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            creation_date DATE
                            )
                       '''
    c.execute(sql_command)


def show_records(c):
    sql_query = '''
                SELECT * FROM credentials_table
                '''
    c.execute(sql_query)
    print(c.fetchall())


def insert_record(c, website, username, password):
    creation_date = ctime()
    sql_command = '''
                    INSERT INTO credentials_table values (?, ?, ?, ?)
                  '''
    c.execute(sql_command, (website, username, password, creation_date))


@authentication
def main():
    conn = connect(DATABASE)
    c = conn.cursor()

    create_table(c)
    insert_record(c, 'coursera', 'juansimon.gr', 'Juanita24')
    show_records(c)

    conn.close()


if __name__ == "__main__":
    main()
