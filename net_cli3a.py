
import netmiko
from netmiko.ssh_exception import NetmikoTimeoutException, SSHException, AuthenticationException
from netmiko import ConnectHandler  # Import the ConnectHandler class

import re

def is_valid_ipv4_address(ip_address):
    pattern = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    match = pattern.match(ip_address)
    return bool(match)

def is_valid_vlan(vlan_id):
    if not isinstance(vlan_id, int):
        return False

    if vlan_id < 1 or vlan_id > 4094:
        return False

    return True

class User:
    def __init__(self, username, password, hostname):
        self.username = username
        self.password = password
        self.hostname = hostname

    def cisco(self):
        cisco = {
            'device_type': 'cisco_ios',
            'username': f'{self.username}',
            'password': f"{self.password}",
            'host': f'{self.hostname}'
        }
        return cisco


class NetConnection:
    def connect(self, cisco):
        try:
            self.net_connect = ConnectHandler(**cisco)  # Initialize net_connect as an instance attribute
            result = "Success"
            #print(result + "_1")  # Print the result


        except AuthenticationException as err:
            error = err
            #print(error)
            return(err)

        #except (AuthenticationException):
        #    result = "Incorrect username or password"
        #    print(result)  # Print the result

        except (NetmikoTimeoutException):
            result = "Timeout to device"
            #print(result)  # Print the result

        except (EOFError):
            result = "End of file while attempting device"
            #print(result)  # Print the result

        except SSHException as err:
            error = err
            #print(error)
            return(err)

        #except(SSHException):
        #    result = "SSH Issue. Are you sure SSH is enabled?"
        #    print(result)  # Print the result

        except Exception as unknown_error:
            result = f"Some other error: {unknown_error}"
            #print(result)  # Print the result










def clearPort2(net_connect, accessPort):
    net_connect.send_command(f"clear port-security stick interface {accessPort}")





def clearPort(self, interface):
    self.net_connect.send_command(f'interface {interface}')
    self.net_connect.send_command("no shutdown")
    self.net_connect.send_command("no shutdown")
    


def changeVlan(self, vlanID):
    self.net_connect.send_command(f'switchport access vlan {vlanID}')
    self.net_connect.send_command("no shutdown")
    self.net_connect.send_command("no shutdown")


def changeVoice(self, voiceVlanID):
    self.net_connect.send_command(f'switchport voice vlan {voiceVlanID}')
    self.net_connect.send_command("no shutdown")
    self.net_connect.send_command("no shutdown")



def showipint(self):
    return self.net_connect.send_command("show ip int brief")




def showver(self):
    output = self.net_connect.send_command("show version")
    print(output)

def showclock(self):
    output = self.net_connect.send_command("show clock")
    print(output)

def showVlan(self):
    output = self.net_connect.send_command("show vlan")
    print(output)

def showauth(self):
    output = self.net_connect.send_command("show authentication")
    print(output)






def changeVoice(voiceVlanID):
    voiceVlan = f'switchport voice vlan {voiceVlanID}'
    return voiceVlan


def saveConfig(net_connect):
    #net_connect.send_command("write memory")
    net_connect.send_command("show ip int brief")


def listCommands():
    commands =[
        f'show ip int brief',
        f'show vlan',
    ]
    return commands







def main():


    user = User("admin", "C1sco12345", "sandbox-iosxe-latest-1.cisco.com")
    cisco = user.cisco()
    net_connect = NetConnection()
    connection_result = net_connect.connect(cisco)  # Call the connect method with the object
    err = None

    userValid = connection_result is None or False
 
    if userValid == True:   # None >>>  No error encountered 
        x = showipint(net_connect)
        print(x)        



        print("===============================")
        #showver(net_connect)
        print("===============================")
        #showclock(net_connect)
        print("===============================")
        #showVlan(net_connect)
        print("===============================")
        print("===============================")
    else:
        print(err)






    '''
    ip_address = "192.168.1.256"
    print(is_valid_ipv4_address(ip_address))
    
    print("===============================")
    print("===============================")

    vlan_id = 100
    print(is_valid_vlan(vlan_id))
    '''



if __name__ == "__main__":
    main()

