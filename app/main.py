import sys
import os
import subprocess
import readline

def get_path(*, all_files=False, only_exec=False):
    """
    Return PATH directories or files contained in those directories.

    Args:
        all_files: If True, return files inside PATH directories.
                   If False, return PATH directories.
        only_exec: If True, return only executable files.
                   Requires all_files=True.
    """
    paths = os.environ.get("PATH", "").split(os.pathsep)

    if not all_files:
        return paths
    
    files = []

    for path in paths:
        if not os.path.isdir(path):
            continue

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            if not os.path.isfile(file_path):
                continue

            if only_exec and not os.access(file_path, os.X_OK):
                continue

            files.append(file)
    
    return files
    
def completer(text, state):
    """this function is used to provide tab completion"""
    if state == 0:
        matches = [c for c in BUILTINS_CMD if c.startswith(text)]
        executable_files = get_path(all_files=True, only_exec=True)
        for file in executable_files:
            if file.startswith(text) and file not in matches:
                matches.append(file)
        matches.sort()
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
    if not parts:
        return None, []
    return parts[0], parts[1:]


def check_executable(command_name):
    """checks if command_name is executable"""
    paths = get_path(all_files=False)
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
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)

# all bultins commands
BUILTINS_CMD = {
    "exit": exit,
    "type": type_cmd,
    "echo": echo,
    "pwd": pwd,
    "cd": cd,
    "clear": clear_screen,
    "cls": clear_screen
}

def display_matches(substitution, matches, longest_match_length):
    print()
    print("  ".join(sorted(matches)))
    print("$ ", end="")
    print(substitution, end="", flush=True)

def main():

    # clear_screen() # clear the screen when the shell starts
    # sys.stdout.write("Welcome to Suman Shell!\n")
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    # im using pyreadline3 on windows, it doesnot support set_completion_display_matches_hook, so i have to check if it exists before calling it
    if hasattr(readline, "set_completion_display_matches_hook"):
        readline.set_completion_display_matches_hook(display_matches)

    while True:
        sys.stdout.write("$ ")

        command = input()
        command_name, args = parse_command(command)

        if command_name is None:
            continue

        if command_name in BUILTINS_CMD:
            BUILTINS_CMD[command_name](*args)
            
        else:
            execute_program(command_name, args)


if __name__ == "__main__":
    main()