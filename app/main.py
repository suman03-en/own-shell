import sys
import os
import subprocess

def parse_command(command: str):
    """
    returns the command name and a list of arguments from the given command string
    """
    parts = command.split()
    return parts[0], parts[1:]

def check_executable(command_name):
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for path in paths:
        file_path = os.path.join(path, command_name)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
    return None

def echo(*args):
    print(f'{" ".join(args)}')

def exit(*args):
    sys.exit(0)

def type_cmd(*args):
    if len(args) < 1:
        return
    for arg in args:
        if arg in BUILTINS:
            print(f"{arg} is a shell builtin")
        else:
            found_path = check_executable(arg)
            if found_path:
                print(f"{arg} is {found_path}")
            else:
                print(f"{arg}: not found")

def execute_program(command_name, args):
    if found_path := check_executable(command_name):
        subprocess.run([command_name] + args)
    else:
        print(f"{command_name}: command not found")
    

BUILTINS = {
    "exit": exit,
    "type": type_cmd,
    "echo": echo
}
def main():

    while True:
        sys.stdout.write("$ ")

        command = input()
        command_name, args = parse_command(command)

        if not command_name:
            continue

        if command_name in BUILTINS:
            BUILTINS[command_name](*args)
            
        else:
            execute_program(command_name, args)

            



if __name__ == "__main__":
    main()