from sqlite3 import connect, OperationalError
from time import ctime, sleep


DATABASE = "credentials.db"
MASTER_PASSWORD = "12345"


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


def user_input():
    user = input("Enter new username: ")
    pswd = input("Enter new password: ")
    date = ctime()
    return (user, pswd, date)


def create_table(c):
    sql_command = '''CREATE TABLE IF NOT EXISTS credentials_table(
                            website TEXT PRIMARY KEY,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            mod_date DATE
                            )'''
    c.execute(sql_command)


def show_records(c):
    website_qry = None
    print("\n*************** DISPLAY OPTIONS ****************\n",
          "--- press 'query' -> display specific record\n"
          "***********************************************\n")

    show_option = input("--> ")
    if show_option == 'query':
        website_qry = input("Enter website fot which to display credentials: ")

    add = f"WHERE website = '{website_qry}'" if website_qry is not None else ''
    sql_query = "SELECT * FROM credentials_table %s" % add

    for record in c.execute(sql_query):
        print(record)

    sleep(1.5)


def insert_record(c):
    website = input("Enter new website: ")

    query = c.execute(f"SELECT * FROM credentials_table WHERE website='{website}'").fetchall()

    if len(query) > 0:
        update_record(c, website)
    else:
        username, password, mod_date = user_input()

        sql_command = "INSERT INTO credentials_table values (?, ?, ?, ?)"
        c.execute(sql_command, (website, username, password, mod_date))


def update_record(c, web=None):
    website = input("Enter website to update: ") if web is None else web
    username, password, mod_date = user_input()

    sql_comand = '''UPDATE credentials_table
                    SET username = ?,
                        password = ?,
                        mod_date = ?
                    WHERE website = ?'''
    c.execute(sql_comand, (username, password, mod_date, website))


def delete_record(c):
    website = input("Password record to be deleted: ")
    sql_command = "DELETE FROM credentials_table WHERE website = '%s'" % website
    c.execute(sql_command)
    print(f"Password for {website} deleted successfully!")


@authentication
def main():
    conn = connect(DATABASE)
    c = conn.cursor()

    create_table(c)

    while True:

        print("\n***************** USER OPTIONS *****************\n",
              "--- press 'i' -> create a new password record\n",
              "--- press 'd' -> delete a password record\n",
              "--- press 'u' -> update an existing record\n",
              "--- press 's' -> display record(s)\n",
              "--- press 'exit' -> exit the script\n",
              "***********************************************\n")
        option = input("-> ")

        if option == 'i':
            insert_record(c)

        elif option == 'd':
            delete_record(c)

        elif option == 'u':
            update_record(c)

        elif option == 's':
            show_records(c)

        elif option == 'exit':
            break

        else:
            print("INVALID OPTION -> Please refer to available user options")

        conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
