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

def execute_program(command_name, args):
    if found_path := check_executable(command_name):
        subprocess.run([command_name] + args)
    else:
        print(f"{command_name}: command not found")

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

def pwd(*args):
    if len(args) >= 1:
        print("Invalid commands, expected 0 args")
        return
    print(os.getcwd()) 

def cd(*args):
    if not args:
        return 
    if len(args) > 1:
        print("Invalid commands, expected 1 arg")
        return
    try:
        os.chdir(args[0])
    except FileNotFoundError as e:
        print(f"cd: {args[0]}: No such file or directory")

def clear_screen(*args):
    if len(args) >= 1:
        print("Invalid commands, expected 0 args")
        return
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)

# all bultins commands
BUILTINS = {
    "exit": exit,
    "type": type_cmd,
    "echo": echo,
    "pwd": pwd,
    "cd": cd,
    "clear": clear_screen
}

def main():

    # clear_screen() # clear the screen when the shell starts
    # sys.stdout.write("Welcome to Suman Shell!\n")

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