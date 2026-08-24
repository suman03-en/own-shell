import sys


def main():
    BUILTINS = ["echo", "exit", "type"]
    while True:
        sys.stdout.write("$ ")
        command = input()
        command_type = command.split()[0]
        if command == "exit":
            break
        if command_type == "echo":
            print(" ".join(command.split()[1:]))
        elif command_type == "type":
            if command.split()[1] in BUILTINS:
                print(f"{command.split()[1]} is a shell builtin")
            else:
                sys.stdout.write(f"{command.split()[1]}: command not found\n")
        else:
            sys.stdout.write(f"{command}: command not found\n")



if __name__ == "__main__":
    main()
