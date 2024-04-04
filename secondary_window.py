import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip

BEIGE = "#F4F1DE"
ORANGE = "#E07A5F"
BLUE = "#3D405B"
GREEN = "#81B29A"
YELLOW = "#F2CC8F"


class SecondaryWindow(tk.Toplevel):
    """Class representing a secondary window with the result."""

    def __init__(self, raw_cmp, cmp, mistakes_list, user_mistakes_words_list, mistake_counter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize window
        self.raw_cmp = raw_cmp
        self.cmp = cmp
        self.wpm = round(self.cmp / 5)
        self.mistakes = mistakes_list
        self.mistake_counter = mistake_counter
        self.user_mistakes_word_list = user_mistakes_words_list
        self.geometry("1700x1100")
        self.resizable(True, True)
        self.config(bg=BEIGE, padx=150, pady=100)
        self.title("Your score")
        self.place_window_center()
        self.style = ttk.Style()
        self.heading_custom_font = font.Font(family="Helvetica", size=25, weight="bold", underline=True)
        self.summary_custom_font = font.Font(family="Microsoft Sans Serif", size=18, weight="normal")

        # Initialize button
        self.button_close = ttk.Button(
            self,
            width=25,
            bootstyle="info",
            padding=10,
            text="Try again",
            command=self.destroy,
        )
        self.button_close.grid(column=2, row=7, sticky="s", pady=30)

        # Initialize header
        self.score_label = ttk.Label(
            self,
            text=f"YOUR SCORE IS {self.cmp} CPM, WHICH IS {self.wpm} WPM.",
            width=50,
            padding=10,
            background=GREEN,
            foreground=BLUE,
            font=self.heading_custom_font,
            anchor="center",
            justify="center",
            underline=1,
        )
        self.style.configure("Custom.TLabel", background=GREEN, foreground=BEIGE, font=("Helvetica", 22))

        # Initialize information icon
        self.info_icon = ttk.Label(self, text="🛈", style="Custom.TLabel")
        ToolTip(self.info_icon,
                text="What are CPM and WPM?\nThey're short for Characters Per Minute, and Words Per Minute. The 'raw"
                     " CPM' is the actual number of characters you type per minute, including all the mistakes. "
                     "'Corrected' scores count only correctly typed words. WPM is just the corrected CPM divided by 5."
                     " That's a de facto international standard.",
                bootstyle="WARNING, INVERSE", wraplength=300)
        self.info_icon.grid(row=1, column=3, sticky="e", padx=10)
        self.score_label.grid(row=1, column=1, columnspan=3, pady=100)
        self.grab_set()

        # Add frame to the window
        self.style.configure("Custom.TLabelframe", bg="#cd9445", background="#cd9445", border=False, relief='flat',
                             labeloutside=False, labelmargins=0, borderwidth=40, foreground=BEIGE,
                             font=self.summary_custom_font)
        self.frame = ttk.LabelFrame(self, style="Custom.TLabelframe")
        self.frame.grid(row=2, column=1, columnspan=3)

        # Add label to the frame
        self.summary_text = ttk.Label(self.frame, width=50, padding=(5, 5), background="#cd9445",
                                      font=self.summary_custom_font, anchor='center', wraplength=1000,
                                      foreground=BEIGE)
        self.summary_text.grid(row=1, column=1, columnspan=3)
        self.show_text_under_score()

    def show_text_under_score(self):
        """
        Function to display text under the score based on mistakes made.
        If mistakes are present, it shows the mistakes made and their corrections.
        If no mistakes, it displays a congratulatory message.
        """
        if self.mistakes:
            self.summary_text.config(text=f'In reality, you typed {self.raw_cmp} CPM, but you made '
                                          f'{self.mistake_counter} mistakes (out of {len(self.mistakes)} words), '
                                          f'which were not counted in the corrected scores.')
            self.summary = ttk.Label(self.frame, text=f"Your mistakes were:", width=60, padding=10, justify='center',
                                     background="#cd9445", font=("Microsoft Sans Serif", 14, "normal"), anchor='center',
                                     wraplength=800,
                                     foreground=BEIGE)
            self.summary.grid(row=2, column=1, columnspan=3)
            self.mistakes_text = ttk.ScrolledText(self.frame, wrap='word', width=60, height=8, bg="#cd9445",
                                                  font=("Helvetica", 12, "normal"))
            # ScrolledText style configuration
            self.mistakes_text.configure(bg="#cd9445", fg=BEIGE, insertbackground="#cd9445")
            self.mistakes_text.tag_configure('error', foreground='red')

            self.mistakes_text.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

            # Filling ScrolledText with text
            for index, word in enumerate(self.mistakes):
                self.mistakes_text.insert('end', f'✿  Instead of "{self.mistakes[index]}", you typed '
                                                 f'"{self.user_mistakes_word_list[index]}"\n')
        else:
            self.summary_text.config(text="✮⋆˙ Congratulations! ✮⋆˙\n You didn't make any mistake!", justify="center",
                                     font=("Microsoft Sans Serif", 20, 'bold'))
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
