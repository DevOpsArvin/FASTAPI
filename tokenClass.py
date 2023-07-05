class TokenClass:
    instances = []

    def __init__(self, name):
        self.name = name
        self.__class__.instances.append(self)

    @classmethod
    def get_TC(cls):
        return cls.instances

    @classmethod
    def generate_TC(cls, name):
        return cls(name)

    @classmethod
    def delete_TC(cls, instance):
        cls.instances.remove(instance)




# Generate instances
# token_account_credentials (tac)
tac = {}


print("==================")
account = "arvin1"
tac[account] = TokenClass.generate_TC(account)

account = "arvin2"
tac[account] = TokenClass.generate_TC(account)

account = "arvin3"
tac[account] = TokenClass.generate_TC(account)


saved_instances2 = TokenClass.get_TC()    

for instance2 in saved_instances2:
    print(instance2.name)
print("==================")

TokenClass.delete_TC(tac["arvin2"])
print("==================")

for instance2 in saved_instances2:
    print(instance2.name)
print("==================")
