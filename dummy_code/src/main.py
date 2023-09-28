from src.utils import greetings
from src.my_class import MyClass


def main():
    my_instance = MyClass('property value')

    my_instance.my_method()
    greetings()


if __name__ == '__main__':
    main()
