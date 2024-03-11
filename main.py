import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import font, messagebox
import random
from secondary_window import SecondaryWindow
from ttkthemes import ThemedTk

# ---------------------------- CONSTANTS ------------------------------- #
BEIGE = "#F4F1DE"
ORANGE = "#E07A5F"
BLUE = "#3D405B"
GREEN = "#81B29A"
YELLOW = "#F2CC8F"
FONT_NAME = "Courier"
WORK_SEC = 60
timer = None
WORDS_LIST = []
CURRENT_WORD = ''
SPACE_COUNT = 0
LETTER_COUNTER = 0
ALL_SIGN_COUNT = 0

# Open 1000 words file and save it as cleaned list
with open("1000 words.txt", "r") as f:
    file = f.readlines()
    list_of_words = [item.strip() for item in file]


def random_words():
    global WORDS_LIST
    WORDS_LIST = [random.choice(list_of_words) for _ in range(80)]
    words_str = " ".join(WORDS_LIST)
    return words_str


def on_entry_click(event):
    if text_entry.get() == "Type the words here.":
        text_entry.delete(0, "end")  # Usuwa tekst zastępczy po kliknięciu
        text_entry.config(foreground=BLUE)  # Zmienia kolor tekstu na czarny


def all_sign_count(word):
    global ALL_SIGN_COUNT
    for _ in word:
        ALL_SIGN_COUNT += 1
        if ALL_SIGN_COUNT % 29 == 0:
            textbox.yview_scroll(1, tk.UNITS)
    print(f"All sign count {ALL_SIGN_COUNT}")
    return ALL_SIGN_COUNT


def space_click(event):
    global CURRENT_WORD, SPACE_COUNT, WORDS_LIST, LETTER_COUNTER, ALL_SIGN_COUNT, start_idx, end_idx
    textbox.tag_remove("green_background", start_idx, end_idx)
    SPACE_COUNT += 1
    CURRENT_WORD = text_entry.get().strip(' ')
    if SPACE_COUNT < len(WORDS_LIST):
        if CURRENT_WORD == WORDS_LIST[SPACE_COUNT - 1]:
            LETTER_COUNTER += len(CURRENT_WORD) + 1
            ALL_SIGN_COUNT = all_sign_count(CURRENT_WORD) + 1
            start_idx = f"1.{ALL_SIGN_COUNT}"
            end_idx = f"1.{ALL_SIGN_COUNT + len(WORDS_LIST[SPACE_COUNT])}"
            textbox.tag_add("green_background", start_idx, end_idx)
        else:
            ALL_SIGN_COUNT = all_sign_count(WORDS_LIST[SPACE_COUNT - 1]) + 1
            start_idx = f"1.{ALL_SIGN_COUNT}"
            end_idx = f"1.{ALL_SIGN_COUNT + len(WORDS_LIST[SPACE_COUNT])}"
            textbox.tag_add("green_background", start_idx, end_idx)
    if text_entry.get() != "":
        text_entry.delete(0, tk.END)


def on_focusout(event):
    if text_entry.get() == '':
        text_entry.insert(0, "Type the words here.")
        text_entry.config(foreground='#BCC1B0')  # Zmienia kolor tekstu na szary


def show_results():
    pass


call_count = 0


def is_valid_key(event):
    # Check if the pressed key is valid (letters, space, backspace, or single quote)
    return event.keysym in ['BackSpace', 'space'] or event.char.isalpha() or event.char == "'"


def reset_call_count():
    # Reset the call count and set the text color to white for the first character
    global call_count
    call_count = 0
    textbox.tag_configure("white_char", foreground='white')
    textbox.tag_add("white_char", '1.0')
    textbox.tag_raise("white_char")


def handle_backspace(char_position):
    # Handle backspace key press by adjusting the call count and restoring the text color
    global call_count, ALL_SIGN_COUNT
    char_index = f"1.{char_position - 1}"
    space_index = textbox.index(f'1.{ALL_SIGN_COUNT - 1}')

    if char_index == space_index:
        return
    elif char_index == '1.-1':
        reset_call_count()
        return
    else:
        call_count -= 1
        char_position -= 1

    textbox.tag_configure("white_char", foreground='white')
    textbox.tag_add("white_char", char_index)
    textbox.tag_raise("white_char")


def track_typing_letters(event):
    # Main function to track typing, validate keys, and update text color accordingly
    global SPACE_COUNT, WORDS_LIST, call_count
    total_characters = sum(len(word) for word in WORDS_LIST) + len(WORDS_LIST) - 1
    char_left = total_characters - call_count
    actual_char_position = total_characters - char_left
    text_entry_word = text_entry.get()

    if SPACE_COUNT < len(WORDS_LIST):
        next_word = WORDS_LIST[SPACE_COUNT]
    else:
        next_word = ""

    counter = 0
    start_index = f"1.{actual_char_position}"

    if not is_valid_key(event):
        # Show a warning if an invalid key is pressed
        messagebox.showwarning("Invalid Key", "You can only use letters, space, and backspace.")
        return

    if counter < len(text_entry_word) and text_entry_word[counter] == " ":
        counter += 1

    # Handle Backspace key press
    if event.keysym == 'BackSpace':
        if call_count == 1:
            handle_backspace(0)
        else:
            handle_backspace(actual_char_position)
        return

    # Handle Space key press
    if event.keysym == 'space':
        call_count = ALL_SIGN_COUNT - 1

    if len(text_entry_word) > len(next_word):
        call_count = ALL_SIGN_COUNT - 1 + len(next_word)

    for char in next_word:
        if counter < len(text_entry_word):
            if char != text_entry_word[counter]:
                textbox.tag_remove("white_char", start_index)
                textbox.tag_remove("blue_char", start_index)
                textbox.tag_add("red_char", start_index)
                textbox.tag_configure("red_char", foreground='#E05E5E')
                counter += 1
            else:
                textbox.tag_remove("white_char", start_index)
                textbox.tag_add("blue_char", start_index)
                textbox.tag_configure("blue_char", foreground='#1C519C')
                counter += 1
    call_count += 1


timer_seconds = 60


def open_secondary_window():
    secondary_window = SecondaryWindow()
    return secondary_window


def countdown_timer():
    global timer_seconds
    if timer_seconds > 0:
        timer_seconds -= 1
        meter.configure(amountused=0 + timer_seconds)
        window.after(1000, countdown_timer)
    else:
        text_entry.config(state="disabled")
        count_points()
        open_secondary_window()


# Funkcja wywołująca się przy wpisaniu pierwszej litery
def on_first_letter(event):
    global timer_seconds
    if timer_seconds == 60:
        # Rozpocznij odliczanie czasu tylko jeśli timer nie jest już uruchomiony
        countdown_timer()


def count_points():
    global ALL_SIGN_COUNT, LETTER_COUNTER, SPACE_COUNT
    raw_cmp = ALL_SIGN_COUNT
    cmp = LETTER_COUNTER
    wpm = round(cmp / 5)
    print(f'raw CMP = {raw_cmp}, CMP = {cmp}, WPM = {wpm}')


window = ttk.Window()
window.title("Typing Speed Test")
window.config(padx=100, pady=50, bg=BEIGE)
flip_timer = window.after(3000, func=show_results)
custom_font = font.Font(family="Arial", size=40, weight="bold", underline=True, slant="roman")
name_label = ttk.Label(
    text="TYPING  SPEED  TEST",
    width=40,
    padding=25,
    background=GREEN,
    foreground=BLUE,
    font=custom_font,
    anchor="center",
)

name_label.grid(row=1, column=1, columnspan=4, pady=100)
style = ttk.Style()

# -------------------------------DISPLAY TEXT WIDGET ------------------------------------------#

textbox = ttk.Text(window, width=120, height=13)
textbox.configure(background=YELLOW, borderwidth=10, border=True, highlightthickness=1, wrap=tk.WORD)
textbox.grid(row=3, column=2, columnspan=2)
textbox.tag_configure("white_char", foreground="white", spacing1=10, spacing2=10, justify='center',
                      font=("Helvetica", 30, 'bold'))
textbox.tag_configure(f"red_char", foreground='#E05E5E', spacing1=10, spacing2=10, justify='center', font=(
    "Helvetica", 30, 'bold'))
textbox.tag_configure(f"blue_char", foreground='#1C519C', spacing1=10, spacing2=10, justify='center', font=
("Helvetica", 30, 'bold'))
textbox.insert(tk.END, random_words())
textbox.tag_config("green_background", background="#BAD46D", borderwidth=2)
start_idx = "1.0"
end_idx = f"1.{len(WORDS_LIST[0])}"
textbox.tag_add("green_background", start_idx, end_idx)

textbox.tag_add("white_char", "1.0", tk.END)

# -------------------------------TEXT ENTRY WIDGET---------------------------------------------#

text_entry = ttk.Entry(window,
                       bootstyle="warning",
                       foreground=BLUE,
                       justify="center",
                       width=50,
                       font=('Helvetica', 22, "bold"))
text_entry.grid(row=4, column=2, columnspan=2)
text_entry.insert(0, "Type the words here.")
text_entry.config(foreground='#BCC1B0')
text_entry.bind('<KeyRelease>', track_typing_letters)
text_entry.bind("<Key>", on_first_letter)
text_entry.bind('<FocusIn>', on_entry_click)
text_entry.bind('<space>', space_click)
text_entry.bind('<FocusOut>', on_focusout)

# -----------------------------TIMER WIDGET ---------------------------------------------------#

meter = ttk.Meter(
    metersize=230,
    stepsize=1,
    amounttotal=60,
    arcrange=360,
    padding=10,
    showtext=True,
    amountused=59,
    metertype="full",
    subtext="seconds left",
    interactive=True,
    bootstyle="info",
    stripethickness=6
)
meter.step(-1)
meter.grid(row=3, column=1, rowspan=2)

window.mainloop()
