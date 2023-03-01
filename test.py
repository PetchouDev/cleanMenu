import sys

from clean_menu import Menu

# test the menu
if __name__ == "__main__":
    menu = Menu("Test", ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "balbalbla"], "A test menu", pointed_background_color="white", pointed_text_color="green", exit_text="Quit me forever...", text_color="magenta", pointer_style=["==>", "<=="], pointer_color="red", title_font="rounded", title_color="blue", margin="        ")
    menu.bind(0, lambda: print("Option 1"))
    menu.bind(1, lambda: print("Option 2"))
    menu.run()  # run the menu