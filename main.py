from multipledispatch import dispatch as override
from colorama import Fore, Back, Style
import sys
import os
import stack

iota_counter = 0


def iota(flag=False):
    global iota_counter
    if flag:
        iota_counter = 0
    res = iota_counter
    iota_counter += 1
    return res


iota(True)

OP_PUSH = iota()
OP_POP = iota()
OP_PLUS = iota()
OP_MINUS = iota()
OP_MUL = iota()
OP_DIV = iota()
OP_MOD = iota()
OP_SQRT = iota()
OP_SWAP = iota()
OP_DUP = iota()
OP_DUMP = iota()

OP_COUNTER = iota()


def push(value) -> tuple:
    return "OP_PUSH", value


def pop():
    return "OP_POP",


def plus():
    return "OP_PLUS",


def minus():
    return "OP_MINUS",


def mul():
    return "OP_MUL",


def sqrt():
    return "OP_SQRT",


def div():
    return "OP_DIV",


def mod():
    return "OP_MOD",


def swap():
    return "OP_SWAP",


def dup():
    return "OP_DUP",


def dump():
    return "OP_DUMP",


def simulate(program: list[str, int]) -> int:
    assert OP_COUNTER == 12, Fore.CYAN + "Some operations are not implemented!"

    base = stack.Stack()

    for op in program:
        try:
            match op[0][0]:
                case "OP_PUSH":
                    base.push(op[0][1])

                case "OP_POP":
                    base.pop()

                case "OP_PLUS":
                    base.push(base.pop() + base.pop())

                case "OP_MINUS":
                    tmp = base.pop()
                    base.push(base.pop() - tmp)

                case "OP_MUL":
                    base.push(base.pop() * base.pop())

                case "OP_SQRT":
                    base.push(base.pop() ** 0.5)

                case "OP_DIV":
                    tmp = base.pop()
                    base.push(base.pop() / tmp)

                case "OP_MOD":
                    tmp = base.pop()
                    base.push(base.pop() % tmp)

                case "OP_SWAP":
                    base.push((base.pop(), base.pop()))

                case "OP_DUP":
                    base.push(base.peek())

                case "OP_DUMP":
                    print(base.peek(), end='\n')
                    base.pop()

        except OverflowError:
            print()
            print(Fore.LIGHTRED_EX +
                  f"{op[1]} : {0} : {op[0][0]} : STACK UNDERFLOW!")
            print(Fore.RED +
                  "PROGRAM TERMINATED!")
            base.debug()
            exit(1)

        except TypeError:
            print()
            print(Fore.LIGHTRED_EX +
                  f"{op[1]} : {0} : {op[0][0]} : TYPE INTERACTION ERROR!")
            print(Fore.RED +
                  "PROGRAM TERMINATED!")
            base.debug()
            exit(1)
    return 0


def compilate(program: list[str, int]) -> int:
    assert OP_COUNTER == 12, Fore.CYAN + "Some operations are not implemented!"

    assert False, Fore.LIGHTRED_EX + "NOT IMPLEMENTED YET!"
    exit(1)


def typeCheck(value) -> type:
    try:
        if int(float(value)):
            if float(value).is_integer():
                return int
            else:
                return float
    except ValueError:
        return str


def parseStrAsOp(string: str, row: int) -> tuple:
    assert OP_COUNTER == 12, Fore.CYAN + "Some operations are not implemented!"

    match string.split():
        case ['//', *_]:
            pass
        case ['push', *args]:
            return push(tuple(typeCheck(val)(val) for val in args)), row
        case ['pop']:
            return pop(), row
        case ['plus']:
            return plus(), row
        case ['minus']:
            return minus(), row
        case ['mul']:
            return mul(), row
        case ['sqrt']:
            return sqrt(), row
        case ['div']:
            return div(), row
        case ['mod']:
            return mod(), row
        case ['swap']:
            return swap(), row
        case ['dup']:
            return dup(), row
        case ['dump']:
            return dump(), row
        case []:
            pass
        case _:
            print()
            print(Fore.LIGHTRED_EX +
                  f"{0} : {op[1]} : UNKHNOWN OPERATOR")
            print(Fore.RED +
                  "PROGRAM TERMINATED!")
            exit(1)


def parseFile(file_path: str) -> list[str, int]:
    with open(file_path, 'r') as file:
        res = [parseStrAsOp(string, row) for row, string in enumerate(file.read().split('\n'))]
    while None in res:
        res.remove(None)
    return res


def checkFilePath(file_path: str) -> bool:
    if os.path.isdir(file_path):
        return False
    if (len(file_path) - file_path.rfind('.oleg')) != 5:
        return False
    return True


def callUsageError(error: str, program=None):
    if program is None:
        print(Fore.YELLOW + "Usage:                                                       \n"
                            "  PROGRAM CALL   --  ./oleg.py FILE_PATH RUN_MODE            \n"
                            "                                                             \n"
                            "  FILE_PATH      --  FILENAME.oleg                           \n"
                            "                                                             \n"
                            "  RUN MODE       --  com (SELF COMPILATION)                  \n"
                            "                 --  sim (PYTHON SIMULATION)                 \n")
    else:
        print(Fore.YELLOW + "Usage:                                                       \n"
                            f"  TRACEBACK      --  {program}                              \n"
                            "  PROGRAM CALL   --  ./oleg.py FILE_PATH RUN_MODE            \n"
                            "                                                             \n"
                            "  FILE_PATH      --  FILENAME.oleg                           \n"
                            "                                                             \n"
                            "  RUN MODE       --  com (SELF COMPILATION)                  \n"
                            "                 --  sim (PYTHON SIMULATION)                 \n")

    print(Fore.RED + error)

    exit(1)


def uncons(data: (list, tuple)) -> tuple:
    return data[0], data[1:]


def argv_parser(argv):
    exit_code = 1

    if len(argv) != 3:
        callUsageError("BAD ARGUMENTS ERROR!")
    program_info, argv = uncons(argv)

    if not checkFilePath(argv[0]):
        callUsageError("FILE_PATH ERROR", program_info)
    file_path, argv = uncons(argv)

    if argv[0] == "sim":
        exit_code = simulate(parseFile(file_path))
    elif argv[0] == "com":
        exit_code = compilate(parseFile(file_path))
    else:
        callUsageError("RUN_MODE ARGUMENTS ERROR", program_info)

    return exit_code


if __name__ == '__main__':
    code = argv_parser(sys.argv)
    exit(code)
