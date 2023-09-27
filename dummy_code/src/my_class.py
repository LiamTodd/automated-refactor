class MyClass:

    def __init__(self, my_prop_renamed):
        self.my_property = my_prop_renamed

    def my_method(self):
        for i in range(len(self.my_property)):
            print(i)
        return 'hello world'
from src.utils.util2 import new_hello
print(new_hello)