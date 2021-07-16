import random
import utils


class Account:
    balance = 0

    def __init__(self, number, pin, balance):
        self.account_number = number
        self.pin = pin
        self.balance = balance

    @classmethod
    def rnd(cls):
        random.seed()
        number = '400000{:09d}'.format(random.randint(0, 999999999))
        checksum = utils.luhns(number)
        account_number = number + str(checksum)
        pin = '{:04d}'.format(random.randint(0, 9999))
        return cls(account_number, pin, 0)

    @classmethod
    def load(cls, number, pin, balance):
        return cls(number, pin, balance)

    def login(self, account, pin):
        return self.account_number == account and self.pin == pin
