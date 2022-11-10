import sys

from clean_menu import Menu

# test the menu
if __name__ == "__main__":
    menu = Menu("Test", ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"])
    menu.bind(0, lambda: print("Option 1"))
    menu.bind(1, lambda: print("Option 2"))
    menu.run()  # run the menu