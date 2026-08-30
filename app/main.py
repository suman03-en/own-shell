import sys
import os
import subprocess
import readline

def completer(text, state):
    """this function is used to provide tab completion"""
    if state == 0:
        matches = [c for c in BUILTINS_CMD if c.startswith(text)]
        completer.matches = matches
    try:
        if len(completer.matches) == 1:
            return completer.matches[state] + " "
        return completer.matches[state]
    except IndexError:
        return None

def parse_command(command: str):
    """
    returns the command name and a list of arguments from the given command string
    """
    parts = command.split()
    try:
        return parts[0], parts[1:]
    except IndexError:
        return parts[0]


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
        if arg in BUILTINS_CMD:
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
    
    dir_path = args[0]

    if args[0] == "~":
        # dir_path = os.environ.get("HOME") # this works for linux and macOS, for windows it will return None, window uses USERPROFILE instead
        dir_path = os.path.expanduser("~") # this works for all platforms
    try:
        os.chdir(dir_path)
    except FileNotFoundError as e:
        print(f"cd: {args[0]}: No such file or directory")
    except Exception as e:
        print(f"cd: {args[0]}: {str(e)}")

def clear_screen(*args):
    if len(args) >= 1:
        print("Invalid commands, expected 0 args")
        return
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)

# all bultins commands
BUILTINS_CMD = {
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
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        sys.stdout.write("$ ")

        command = input()
        command_name, args = parse_command(command)

        if not command_name:
            continue

        if command_name in BUILTINS_CMD:
            BUILTINS_CMD[command_name](*args)
            
        else:
            execute_program(command_name, args)


if __name__ == "__main__":
    main()