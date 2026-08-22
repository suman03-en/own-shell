import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    command = input()
    sys.stdout.write(f"{command}: Command not found")


if __name__ == "__main__":
    main()
