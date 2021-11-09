class M(type):
    @classmethod
    def __prepare__(cls, *args):
        class CustomDict(dict):
            def __repr__(self): return "I am a custom dict: " + str(id(self))
        namespace = CustomDict()
        print('From __prepare__ namespace: {}'.format(namespace))
        return namespace

    def __new__(metacls, name, bases, namespace):
        print("From __new__ namespace {}".format(namespace))
        return super().__new__(metacls, name, bases, namespace)


class Test(metaclass=M):
    def __init__(self):
        print('In __init__ of Test')


t = Test()

print(dir(t))