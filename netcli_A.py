from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def doit(host, user, password):

    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": user,
        "password": password,
    }
    
    '''
    Xcommands = [
        'sh ip int brie',
        'show vlans'
    ]

    Zcommands =[
        f'interface {interface}',
        f'switchport access vlan {vlanID}',
        'shutdown',
        'no shutdown'
        'write memory'
    ]
    '''

    commands =[
        'interface fa0/18',
        'shutdown',
        'no shutdown'
    ]

    
    result = {}
    err = ""
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output

        print(output)
        print("Done Successfully...")
        
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        err = f"line 22: {error} "
        print(err)


def main():

    '''
    host =  "sandbox-iosxr-1.cisco.com"
    username = "admin"
    password = "C1sco12345"
    '''

    host =  "10.16.0.227"
    username = "a.acosta"
    password = "!@Rvin#8569"


    
    # Call the doit function
    result = doit(host, username, password)
    
    # Process the result as needed
    print(result)


if __name__ == "__main__":
    main()
