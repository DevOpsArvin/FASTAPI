class MyClass:
    instances = []

    def __init__(self, name):
        self.name = name
        self.__class__.instances.append(self)

    @classmethod
    def get_instances(cls):
        return cls.instances

    @classmethod
    def generate_instance(cls, name):
        return cls(name)

    @classmethod
    def remove_instance(cls, instance):
        cls.instances.remove(instance)

# Generate instances
data = {}

# Assigning values to keys
data["ako1"] = MyClass.generate_instance("ako11")
data["ako2"] = MyClass.generate_instance("ako22")
data["ako3"] = MyClass.generate_instance("ako33")
saved_instances2 = MyClass.get_instances()

# Printing all key-value pairs
for instance2 in saved_instances2:
    print(instance2.name)

MyClass.remove_instance(data["ako2"])
print("==================")


data["ako4"] = MyClass.generate_instance("ako44")
saved_instances2 = MyClass.get_instances()    

for instance2 in saved_instances2:
    print(instance2.name)


