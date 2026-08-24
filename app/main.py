import sys
import os


def main():
    BUILTINS = ["echo", "exit", "type"]

    while True:
        sys.stdout.write("$ ")

        command = input()
        parts = command.split()

        if not parts:
            continue

        command_type = parts[0]

        if command_type == "exit":
            break

        elif command_type == "echo":
            print(" ".join(parts[1:]))

        elif command_type == "type":
            if len(parts) < 2:
                continue

            command_name = parts[1]

            if command_name in BUILTINS:
                print(f"{command_name} is a shell builtin")
                continue

            found = None

            paths = os.environ.get("PATH", "").split(os.pathsep)

            for path in paths:
                file_path = os.path.join(path, command_name)

                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    found = file_path
                    break

            if found:
                print(f"{command_name} is {found}")
            else:
                print(f"{command_name}: not found")

        else:
            print(f"{command_type}: command not found")


if __name__ == "__main__":
    main()