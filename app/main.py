import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        if command.split()[0] == "echo":
            print(" ".join(command.split()[1:]))
        else:
            sys.stdout.write(f"{command}: command not found\n")



if __name__ == "__main__":
    main()
