import mysql.connector
import os, hashlib, uuid, getpass


class myDB(object):
    _db_connection = None
    _db_cursor = None 

    def __init__(self):
        try:
            self._db_connection = mysql.connector.connect(user='root', password ='lqkwje', host = '127.0.0.1', database = 'users')
        except mysql.connector.Error as err:
            print('Cannot connect to DB!')
            print(err)
        else:
            self._db_cursor = self._db_connection.cursor(buffered = True)

    def query(self, query, params):
        try: 
            result = self._db_cursor.execute(query, params)
        except BaseException as error:
            print('Some error occured: {}'.format(error))
        else:
            self._db_connection.commit()
            return result
    
    def getonevalue(self):
        """
        This method gets a value from DB cursor
        Row and field represent row and field in DB 
        """
        for row in self._db_cursor:
            for field in row:
                return field

    def __del__(self):
        self._db_cursor.close()
        self._db_connection.close()

class myApp(object):
    def showMenu(self):
        print("""What do you wanna do?
             1.create a new user
             2.Open existing user
             3.exit""")


def hashpassword(password):
    salt = uuid.uuid4().hex.encode('utf-8')
    password = password.encode('utf-8')
    hashed_passw = hashlib.sha256(password + salt).hexdigest()
    results = [salt, hashed_passw] 
    print(results)
    return results

def newuser():
    name = str(input('Your username: '))
    select_users = ("SELECT username FROM users")
    existence = None
    db.query(select_users, '')
    for row in db._db_cursor:
        for field in row:
            if name == field:
                existence = 1
    if existence == 1:
        print('Name already exist in DB!\n')
    else:
        passw= str(input('Your new password: '))
        password = hashpassword(passw)
        add_newuser = ("INSERT INTO users "
                      "(id, username, password, salt) "
                      "VALUES (%s, %s, %s, %s)")
        data_newuser = ('', name, password[1], password[0])
        db.query(add_newuser, data_newuser)
        print('New user created\n')


if __name__ == '__main__':
    global db
    db = myDB()
    app = myApp()
    while True:
        app.showMenu()
        try:
            choice = int(input('Your choice?: '))
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Your response must be a number 1 or 2 or 3')
            continue

        if choice not in (1, 2, 3):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Your response must be a number 1 or 2 or 3')
            continue
        elif choice == 1:
            newuser()
            continue
        elif choice == 2:
            user = str(input('Enter your username: '))
            query = ("SELECT username FROM users WHERE username = %s")
            db.query(query, (user, ))
            name = db.getonevalue()
            if name  == user:
                print(name)
                attempts = 0
                while attempts < 3:
                    passwd_input = getpass.getpass('Your password: ')
                    query = ('SELECT id, password, salt FROM users WHERE username = %s') 
                    cursor.execute(query, (user,))
                    passwrow = cursor.fetchone()
                    salt = passwrow[2].encode('utf-8')
                    passwd_input = passwd_input.encode('utf-8')
                    hashed = hashlib.sha256(passwd_input + salt).hexdigest()
                    print(hashed)
                    print(passwrow)
                    if hashed == passwrow[1]:
                        print('Youre in ')
                        cursor.reset()
                        query = ('SELECT site_name, site_password FROM collections WHERE id_user = %s')
                        cursor.execute(query, (passwrow[0],))
                        sites = cursor.fetchall()
                        print(sites)
                    else: attempts = attempts + 1   
        else:
            db._db_cursor.close()
            db._db_connection.close()
            quit()

