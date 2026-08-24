import sys
import os


def main():
    BUILTINS = ["echo", "exit", "type"]

    while True:
        found = None
        sys.stdout.write("$ ")
        command = input()
        command_type = command.split()[0]
        if command_type == "exit":
            break
        elif command_type == "echo":
            print(" ".join(command.split()[1:]))

        elif command_type == "type":
            if command.split()[1] in BUILTINS:
                print(f"{command.split()[1]} is a shell builtin")
            else:
                paths = os.environ.get("PATH").split(os.pathsep)
                for path in paths:
                    if found:
                        break
                    files = os.listdir(path)
                    for file in files:
                        file_path = os.path.join(path, file)
                        file_name = file.rsplit(".")[0]
                        if file_name == command.split()[1] and os.access(file_path, os.X_OK): 
                            found = file_path
                            break     
                if found:
                    sys.stdout.write(f"{command.split()[1]} is {found}\n")
                else:
                    sys.stdout.write(f"{command.split()[1]}: not found\n")
        else:
            sys.stdout.write(f"{command}: command not found\n")



if __name__ == "__main__":
    main()
