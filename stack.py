from multipledispatch import dispatch as override


class Stack:
    def __init__(self):
        self.__data = []
        self.__capacity = 0

    @override((int, float, str))
    def push(self, value) -> None:
        self.__data.append(value)
        self.__capacity += 1

    @override((list, tuple))
    def push(self, data) -> None:
        self.__data.extend(data)
        self.__capacity += len(data)

    def pop(self):
        if self.__capacity <= 0:
            raise OverflowError
        self.__capacity -= 1
        return self.__data.pop()

    def peek(self):
        if self.__capacity <= 0:
            raise OverflowError
        return self.__data[-1]

    def isEmpty(self) -> bool:
        return __capacity > 0

    def getSize(self) -> int:
        return self.__capacity

    def debug(self):
        for el in self.__data:
            print(f'{el}\n')
