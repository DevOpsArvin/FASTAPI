class Account:
    instances = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__class__.instances[username] = self

    @classmethod
    def get_account(cls, username):
        return cls.instances.get(username)

    @classmethod
    def create_account(cls, username, password):
        return cls(username, password)

    @classmethod
    def delete_account(cls, username):
        if username in cls.instances:
            del cls.instances[username]





# Generate instances
accounts = {}

print("==================")
account = "user1"
password = "password1"
accounts[account] = Account.create_account(account, password)

account = "user2"
password = "password2"
accounts[account] = Account.create_account(account, password)

account = "user3"
password = "password3"
accounts[account] = Account.create_account(account, password)

# Print all account instances
for account_instance in Account.instances.values():
    print(f"account: {account_instance.username} {account_instance.password}")


print("1==================")



user = 'user1'
account_instance = Account.get_account(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")

user = 'user2'
account_instance = Account.get_account(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")


print("2==================")



Account.delete_account('user2')
print("3==================")



user = 'user2'
account_instance = Account.get_account(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")
print("4==================")


user = 'user1'
account_instance = Account.get_account(user)
if account_instance:
    password = account_instance.password
    print(f"account: {user} {password}")
else:
    print("Account not found.")
print("4==================")

