from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


class TokenAccount:
    instances = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.instances[username] = self

    def get_account(self, username):
        return self.instances.get(username)

    def create_account(self, username, password):
        return TokenAccount(username, password)

    def delete_account(self, username):
        if username in self.instances:
            del self.instances[username]


UsersLoggedIn = {}  # Define the UsersLoggedIn dictionary


def login(username: str, password: str):
    device = {
        "device_type": "cisco_ios",
        "host": "sandbox-iosxr-1.cisco.com",
        "username": username,
        "password": password,
    }
    return validate_login(device, [])


def validate_login(device, commands):
    result = {}
    try:
        username = device["username"]
        password = device["password"]

        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output

        print("Login Successful - Proceed to Search")
        print(f"54=======: {username} {password}")

        # Add the logged-in user to UsersLoggedIn dictionary
        UsersLoggedIn[username] = TokenAccount(username, password)

        # Print all account instances
        for account_instance in TokenAccount.instances.values():
            print(f"62=======: {account_instance.username} {account_instance.password}")

        user = 'admin1'
        account_instance = UsersLoggedIn.get(user)
        if account_instance:
            password = account_instance.password
            print(f"66=======: {user} {password}")
        else:
            print("Account not found.")

        return True

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        return False


# Prompt for username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Call the login function with the provided username and password
result = login(username, password)
