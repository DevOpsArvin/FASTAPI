from pprint import pprint

import yaml
import getpass

import webbrowser

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output

        print("Login Successfull - Proceed to Search")
        url = "https://getbootstrap.com/docs/4.0/content/tables/"
        webbrowser.open(url)
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

def get_user_credentials():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return username, password


def main():
    username, password = get_user_credentials()

    device = {
        "device_type": "cisco_ios",
        "host": "sandbox-iosxr-1.cisco.com",
        "username": username,
        "password": password,
    }
    #result = send_show_command(device, ["sh ip int br"])
    result = send_show_command(device, [])
    pprint(result, width=120)

if __name__ == "__main__":
    main()
