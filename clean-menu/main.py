import os
import sys

from termcolor import colored, cprint
import colorama
from art import text2art as t2a
from pynput.keyboard import Key, Listener, Controller
import platform

colorama.init()


# create a menu object class
class Menu:
    def __init__(self,
                 title,  # menu title
                 options,  # list of options
                 exit_text="Exit",  # exit text
                 exit_function=sys.exit,  # exit function called when
                 art_title=True,  # enable/disable ascii art title
                 title_font="",  # ascii art title font
                 default_pointer_index=0,  # default option index in option list
                 margin="    ",  # characters before options, better result when longer than pointer
                 title_color="red",  # title color
                 text_color="white",  # color for not pointed options
                 pointer_style=None,  # pointer style, if None, no pointer
                 pointer_color="green",  # pointer color
                 pointed_text_color="white",  # pointed option text color
                 pointed_background_color="None",  # pointed option background color
                 ):
        self.title = colored(title, title_color) if art_title is False else colored(t2a(title, font=title_font), title_color)
        self.options = options if exit_text is None else options + [exit_text]
        self.pointer = default_pointer_index
        if not 0 <= self.pointer <= len(self.options) - 1:
            self._error_message("Menu Error", "Default pointer index out of range")
            raise IndexError
        self.margin = margin
        self.title_color = title_color
        self.text_color = text_color
        self.pointer_color = pointer_color
        if pointer_style is None:
            self.pointer_style = ""
            self.pointer_len = 0
        else:
            self.pointer_style = [colored(p, pointer_color, f"on_{pointed_background_color}") for p in pointer_style]
            self.pointer_len = len(pointer_style[0]) if isinstance(pointer_style, list) else len(pointer_style)
        self.pointed_text_color = pointed_text_color
        self.pointed_background_color = pointed_background_color
        self.actions = {str(i): i for i in range(len(self.options) - 1)}
        if exit_text in self.options:
            self.actions[str(self.options.index(exit_text))] = exit_function
        self.has_exit = True if exit_text in self.options else False

    # displays the menu
    def _print(self):
        # clear the screen
        a = os.system("cls" if platform.system() == "Windows" else "clear")
        print(self.title)
        for i in range(len(self.options)):
            if i == self.pointer:
                self._print_pointed()
            else:
                cprint(self.margin + self.options[i], self.text_color)

    def _print_pointed(self):
        # if pointer is a list
        if isinstance(self.pointer_style, list) and len(self.pointer_style) >= 2:
            pointer_left = self.pointer_style[0]
            pointer_right = self.pointer_style[1]

            pointed_text = (self.margin[:len(self.margin) - self.pointer_len]
                            + pointer_left
                            + colored(
                self.options[self.pointer], self.pointed_text_color,
                f"on_{self.pointed_background_color}"
            )
                            + pointer_right,
                            self.pointer_color)[0]
            print(pointed_text)

        else:
            cprint(self.margin + self.options[self.pointer], self.pointer_color)

    # actions on key press
    # listen for arrows up and down
    def _on_press(self, key):
        if key == Key.up and self.running is True:
            # point to upper item
            self.pointer = self.pointer - 1 if self.pointer > 0 else len(self.options) - 1
            self._print()
        if key == Key.down and self.running is True:
            # point to lower item
            self.pointer = self.pointer + 1 if self.pointer < len(self.options) - 1 else 0
            self._print()
        if key == Key.enter and self.running is True:
            # prevent from running previous commands
            c = Controller()
            self.running = False
            for _ in range(100):
                c.press(Key.down)
                c.release(Key.down)
            del c
            self.listener.stop()

    def bind(self, option_index, func):
        offset = 2 if self.has_exit is True else 1
        if 0 <= option_index <= len(self.options) - offset:
            self.actions[str(option_index)] = func
        else:
            self._error_message("Bind Error", "Index out of range")
            print("List of available options to assign functions :")
            for i in range(len(self.options) - (offset - 1)):
                print(f"{i} : {self.options[i]}")
            raise IndexError

    def _error_message(self, title, message):
        print(f"{colored(title, 'red')}: {message}")

    def _run(self):
        self._print()
        self.running = True
        self.listener = Listener(on_press=self._on_press)
        self.listener.start()
        self.listener.join()
        return self.pointer

    def get_index(self):
        return self._run()

    def run(self):
        return self.actions[str(self._run())]()


def example():
    print("Example function")
    menu = Menu("Test",
                ["Option 1", "Option 2", "Option 3"],
                title_font="rounded",
                title_color="blue",
                margin="        ",
                pointer_style=["==>", "<=="],
                pointer_color="red",
                pointed_background_color="white",
                pointed_text_color="green",
                exit_text="Quit me forever...",
                text_color="magenta",
                )

    menu.bind(0, lambda: print("Option 1"))
    menu.bind(1, lambda: print("Option 2"))
    menu.bind(2, lambda: print("Option 3"))
    menu.bind(3, lambda: print("Option 4"))

    menu.run()


if __name__ == "__main__":
    example()