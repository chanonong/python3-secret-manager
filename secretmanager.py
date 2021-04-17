import sqlite3

class Secret:
    def __init__(self, user_id, secret_type, secret_value):
        self.user_id = user_id
        self.secret_type = secret_type
        self.secret_value = secret_value

class SecretManager:
    def __init__(self, db_file_name):
        self.connection = sqlite3.connect(db_file_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
                        '''CREATE TABLE IF NOT EXISTS secrets (secret_id integer primary key autoincrement, user_id text, secret_type text, secret_value text)''')
    
    def save_secret(self, secret):
        print(f'check: {secret.__dict__}')
        self.cursor.execute('SELECT user_id, secret_type FROM secrets WHERE user_id = ? AND secret_type = ?', (secret.user_id, secret.secret_type))
        result = self.cursor.fetchone()
        if result:
            print(f'update: {secret.__dict__}')
            self.cursor.execute('UPDATE secrets SET secret_value = ? WHERE user_id = ? AND secret_type = ?', (secret.user_id, secret.secret_type, secret.secret_value))
            self.connection.commit()
        else:
            print(f'add: {secret.__dict__}')
            self.cursor.execute('INSERT INTO secrets (user_id, secret_type, secret_value) VALUES (?, ?, ?)', (secret.user_id, secret.secret_type, secret.secret_value))
            self.connection.commit()

    def delete_secret(self, user_id, secret_type):
        self.cursor.execute('DELETE FROM secrets WHERE user_id = ? AND secret_type = ?', (user_id, secret_type))
        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM secrets WHERE user_id = ?', (user_id,))
        self.connection.commit()

    def is_user_register(self, user_id):
        self.cursor.execute('SELECT user_id FROM secrets WHERE user_id=?', (user_id,))
        result = self.cursor.fetchone()
        print(result)
        return result is not None
    
    def get_user_secrets_as_dict(self, user_id):
        self.cursor.execute('SELECT user_id, secret_type, secret_value FROM secrets WHERE user_id=?', (user_id,))
        results = self.cursor.fetchall()
        secret_dict = dict()
        for i, k, v in results:
            secret_dict[k] = v
        return secret_dict

if __name__ == '__main__':
    sm = SecretManager('testdb.db')
    s1 = Secret('u1','a','b')
    s2 = Secret('u1','c','d')
    sm.save_secret(s1)
    sm.save_secret(s2)
    print(sm.get_user_secrets_as_dict('u1'))
