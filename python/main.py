from pathlib import Path

import Organize
import Reversal
from Reversal import LogFileError


def main():
    if Path("FOLog.txt").exists():
        choice = input("1. Organize\n2. Reverse Previous Session\n> ")
        if choice == '1' or choice == "Organize":
            Organize.start()
        elif choice == '2' or choice == "Reverse Previous Session":
            try:
                Reversal.start()
            except LogFileError as e:
                print(e)
        else:
            print("Try again.")
            main()
    else:
        Organize.start()
    input("\nPress enter to close")


if __name__ == "__main__":
    main()
