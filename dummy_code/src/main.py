from src.utils import my_func
from src.my_class import MyClass

def main():
    my_instance = MyClass("property value")
    my_instance.my_method()
    my_func()

if __name__ == "__main__":
    main()