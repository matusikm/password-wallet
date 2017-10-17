import mysql.connector
import os, hashlib, uuid, getpass

def showMenu():
    print("""What do you wanna do?
         1.create a new user
         2.Open existing user
         3.exit""")
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
            self._db_cursor = self._db_connection.cursor()

    def query(self, query, params):
        try: 
            result = self._db_cursor.execute(query, params)
        except BaseException as error:
            print('Some error occured: {}'.format(error))
        else:
            self._db_connection.commit()
            return result

    def __del__(self):
        self._db_cursor.close()
        self._db_connection.close()

def hashpassword(password):
    salt = uuid.uuid4().hex.encode('utf-8')
    password = password.encode('utf-8')
    hashed_passw = hashlib.sha256(password + salt).hexdigest()
    results = [salt, hashed_passw] 
    print(results)
    return results

def newuser():
    name = str(input('Your username: '))
    passw= str(input('Your new password: '))
    password = hashpassword(passw)
    add_newuser = ("INSERT INTO users "
                  "(id, username, password, salt) "
                  "VALUES (%s, %s, %s, %s)")
    data_newuser = ('', name, password[1], password[0])
    db.query(add_newuser, data_newuser)

def program():
    global db
    db = myDB()
    while True:
        showMenu()
        try:
            a = int(input('Your choice?: '))
        except ValueError:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Your response must be a number 1 or 2 or 3')
            continue

        if a not in (1, 2, 3):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Your response must be a number 1 or 2 or 3')
            continue
        elif a == 1:
            newuser()
            print('ok')
            continue
        elif a == 2:
            user = str(input('Enter your username: '))
            cnx = dbconnect()
            cursor = cnx.cursor(buffered = True)
            query = ("SELECT username FROM users")
            cursor.execute(query)
            for row in cursor:           #we get a tulpes representing a row in db
                for field in row:        #we go throug every tulpe to get username
                    if field == user:
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
            #cursor.close()
            #cnx.close()
        else:
            quit()

program()
#hashpassword('wfekwkejf')
