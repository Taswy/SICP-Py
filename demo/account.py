# coding=utf-8

class Account(object):
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance
    def withdraw(self, amount):
        if self.balance < amount:
            return 'Insufficent funds'
        self.balance = self.balance - amount
        return self.balance