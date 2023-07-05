class Account:
    instances = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.instances[username] = self

    def get_account(self, username):
        return self.instances.get(username)

    def create_account(self, username, password):
        return Account(username, password)

    def delete_account(self, username):
        if username in self.instances:
            del self.instances[username]


# Generate instances
accounts = {}

print("==================")
account = "user1"
password = "password1"
accounts[account] = Account(account, password)

account = "user2"
password = "password2"
accounts[account] = Account(account, password)

account = "user3"
password = "password3"
accounts[account] = Account(account, password)

# Print all account instances
for account_instance in Account.instances.values():
    print(f"account: {account_instance.username} {account_instance.password}")

print("1==================")

user = 'user1'
account_instance = accounts[user]
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")

user = 'user2'
account_instance = accounts[user]
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")

print("2==================")

# Delete the account from both instances and accounts dictionary
accounts['user2'].delete_account('user2')
del accounts['user2']
print("3==================")


user = 'user2'
account_instance = accounts.get(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")

print("4==================")

user = 'user1'
account_instance = accounts.get(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")

print("4==================")
