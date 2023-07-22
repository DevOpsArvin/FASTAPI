
import netmiko
from netmiko.ssh_exception import NetmikoTimeoutException, SSHException, AuthenticationException
from netmiko import ConnectHandler  # Import the ConnectHandler class



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


def showVlan(self):
    return self.net_connect.send_command("show vlan")




def clearMe(uname, pswd, host):
    user = User(uname, pswd, host)
    cisco = user.cisco()
    net_connect = NetConnection()
    connection_result = net_connect.connect(cisco)  # Call the connect method with the object
    err = None

    userValid = connection_result is None or False
 
    if userValid == True:   # None >>>  No error encountered 
        x = showipint(net_connect)
        print(x)        

    else:
        print(err)



def clearMe2(uname, pswd, host):
    user = User(uname, pswd, host)
    cisco = user.cisco()
    net_connect = NetConnection()
    connection_result = net_connect.connect(cisco)  # Call the connect method with the object
    err = None

    userValid = connection_result is None or False
 
    if userValid == True:   # None >>>  No error encountered 
        x = showVlan(net_connect)
        print(x)        

    else:
        print(err)







def main():

    clearMe("admin", "C1sco12345", "sandbox-iosxe-latest-1.cisco.com")
    clearMe2("admin", "C1sco12345", "sandbox-iosxe-latest-1.cisco.com")


if __name__ == "__main__":
    main()

