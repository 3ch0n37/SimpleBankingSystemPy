import sqlite3
from account import Account


class Bank:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.conn.row_factory = sqlite3.Row
        try:
            cur = self.conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0);''')
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print('DB error: ' + str(e))

    def new_account(self):
        cur = self.conn.cursor()
        account = Account.rnd()
        cur.execute('insert into card (number, pin) values (:number, :pin)',
                    {'number': account.account_number, 'pin': account.pin})
        self.conn.commit()
        return account

    def find_account(self, number):
        cur = self.conn.cursor()
        cur.execute('select * from card where number = ?', [number])
        res = cur.fetchone()
        if not res:
            return None
        return Account.load(res['number'], res['pin'], res['balance'])

    def add_income(self, to, amount):
        cur = self.conn.cursor()
        try:
            cur.execute('update card set balance=:balance where number = :number',
                        {'number': to.account_number, 'balance': to.balance + amount})
            self.conn.commit()
            return True
        except sqlite3.DatabaseError:
            return False

    def do_transfer(self, sender, receiver, amount):
        if sender.balance < amount:
            return -1
        elif sender.account_number == receiver.account_number:
            return 0
        cur = self.conn.cursor()
        try:
            cur.executemany('update card set balance = ? where number = ?', [
                [sender.balance - amount, sender.account_number],
                [receiver.balance + amount, receiver.account_number]
            ])
            self.conn.commit()
            return True
        except sqlite3.DatabaseError:
            return False

    def close_account(self, account):
        cur = self.conn.cursor()
        try:
            cur.execute('delete from card where number = ?', [account.account_number])
            self.conn.commit()
            return True
        except sqlite3.DatabaseError:
            return False
