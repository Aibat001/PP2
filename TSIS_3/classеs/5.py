class Account:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance
    def __str__(self):
        return f'Account owner: {self.owner}\nAccount balance: {self.balance}'
    def deposit(self, dep_amt):
        self.balance += dep_amt
        print("Deposit Accepted")
    def withdraw(self, wd_amt):
        if self.balance >= wd_amt:
            self.balance -= wd_amt
            print("Withdraw Accepted")
        else:
            print("Withdraw not Accepted")
        return Account(self.owner, self.balance)


acct1 = Account(input(), int(input()))
print(Account.withdraw(acct1, int(input())))
acct1.owner
acct1.balance
acct1.deposit(50)
acct1.withdraw(75)
acct1.withdraw(500)
