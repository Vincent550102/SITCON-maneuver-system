import sqlite3
import json

with open('config.json', 'rb') as (jsonfile):
    config = json.load(jsonfile)


class Database():
    def __init__(self):
        self.con = sqlite3.connect(
            'database/sqlite.db', check_same_thread=False)
        self.cur = self.con.cursor()
        sql_init = open('database/init.sql', 'r').read()
        self.con.executescript(sql_init)
        self.con.commit()
        for username in config['usernames']:
            if not self.get_status_by_username(username):
                self.insert_status_by_username(username, '閒置中')

    def __del__(self):
        self.con.close()

    def init_status(self):
        for username in config['usernames']:
            self.update_status_by_username(username, '閒置中')

    def get_all_status(self):
        self.cur.execute('SELECT * FROM manstatus')
        return self.cur.fetchall()

    def get_status_by_username(self, username):
        self.cur.execute(
            'SELECT status FROM manstatus WHERE username=?', (username,))
        try:
            return self.cur.fetchone()[0]
        except TypeError:
            return None

    def insert_status_by_username(self, username, status):
        self.cur.execute('INSERT INTO manstatus (username, status) VALUES (?, ?)',
                         (username, status))
        self.con.commit()

    def update_status_by_username(self, username, status):
        self.cur.execute('UPDATE manstatus SET status=? WHERE username=?',
                         (status, username))
        self.con.commit()


# if __name__ == '__main__':
    # database = Database()
    # database.update_status_by_username('Vincent550102', '守門中')
    # print(database.get_all_status())
