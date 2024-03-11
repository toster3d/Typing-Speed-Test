import tkinter
from tkinter import ttk


class SecondaryWindow(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=300, height=300)
        self.title("Your score")
        self.button_close = ttk.Button(
            text="Close window",
            command=self.destroy
        )
        self.button_close.grid(column=1, row=1)
        self.focus()
        self.grab_set()
        self.place_window_center()

    def place_window_center(self):
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')
