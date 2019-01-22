# coding=utf-8

class Account(object):
    interest = 0.02 # 类变量/静态变量， 如果某个对象在后面动态覆盖掉这个值，会产生一个同名的引用，但不会影响其他对象
    def __init__(self, account_holder):
        self.balance = 0 # 对象的变量
        self.holder = account_holder
    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance
    def withdraw(self, amount):
        if self.balance < amount:
            return 'Insufficent funds'
        self.balance = self.balance - amount
        return self.balance

class CheckingAccount(Account):
    """A bank account that charges for withdrawals."""
    withdraw_charge = 1
    interest = 0.01
    def withdraw(self, amount): # 先查找CheckingAccount中的方法再查找Account中的方法，找到之后再将方法绑定到CheckingAccount的实例上的self进行调用，而不是Account的实例
        return Account.withdraw(self, amount + self.withdraw_charge) # 使用self.withdraw_charge是因为这个值可能动态地覆盖掉原静态值

class SavingsAccount(Account):
    deposit_charge = 2
    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_charge)

class AsSeenOnTVAccount(CheckingAccount, SavingsAccount):
    """多重继承,将活期存款和储蓄账户的特点合而为一"""
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 1 # A free dollar!