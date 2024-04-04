import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font, messagebox
import random
from secondary_window import SecondaryWindow
from healpers import is_valid_key

# ---------------------------- CONSTANTS ------------------------------- #
BEIGE = "#F4F1DE"
BLUE = "#3D405B"
GREEN = "#81B29A"
YELLOW = "#F2CC8F"
WORK_SEC = 60
WORDS_LIST = []
CURRENT_WORD = ''
SPACE_COUNT = 0
LETTER_COUNTER = 0
ALL_SIGN_COUNT = 0
tracking_function_call_count = 0
MISTAKE_WORDS = []
USER_MISTAKES = []

# Open 1000 words file and save it as cleaned list
try:
    with open("1000 words.txt", "r") as f:
        file = f.readlines()
        list_of_words = [item.strip() for item in file]
except FileNotFoundError:
    messagebox.showerror("The file '1000 words.txt' was not found.")

# Check the uniqueness of words and remove duplicates if necessary
if len(set(list_of_words)) != len(list_of_words):
    list_of_words = list(set(list_of_words))


def random_words():
    """
    Function that generates a random string of 200 words.

    This function selects 200 words randomly from the list_of_words and joins them into a single string.
    Returns:
     - A string containing the randomly selected 200 words.
    """
    global WORDS_LIST
    WORDS_LIST = [random.choice(list_of_words) for _ in range(200)]
    words_str = " ".join(WORDS_LIST)
    return words_str


def on_entry_click(event):
    """
      Event handler for the click event on the text entry field.
      This function is triggered when the text entry field is clicked. It performs the following actions:
      - If the text entry field contains the default text placeholder, it clears the text and changes the text color to black.
      Parameters:
      event (Event): The click event object.
      Returns:
      None
      """
    if text_entry.get() == "Type the words here.":
        text_entry.delete(0, "end")
    text_entry.config(foreground=BLUE)


def on_focusout(event):
    """
    Event handler for the focus out event on the text entry field.
    This function is triggered when the text entry field loses focus. It performs the following actions:
    - Clears the entire text from the text entry field.
    - Inserts the default text placeholder.
    - Changes the text color to gray.
    Parameters:
    - event (Event): The focus out event object.
    Returns:
    - None
    """
    text_entry.delete(0, "end")
    text_entry.insert(0, "Type the words here.")
    text_entry.config(foreground='#BCC1B0')


def scroll_textbox():
    """
    Scrolls the textbox by one unit if the total sign count is a multiple of 32.
    Returns:
    - None
    """
    if ALL_SIGN_COUNT % 32 == 0:
        textbox.yview_scroll(1, tk.UNITS)


def all_sign_count(word):
    """
    Counts all characters in the given word and updates the global variable ALL_SIGN_COUNT.

    This function iterates through each character in the word and increments the ALL_SIGN_COUNT variable by 1 for each character.
    If the total count is a multiple of 32, it scrolls the textbox.
    Parameters:
    word (str): The word for which characters will be counted.
    Returns:
    int: The total count of characters.
    """
    global ALL_SIGN_COUNT
    for _ in word:
        ALL_SIGN_COUNT += 1
        scroll_textbox()
    return ALL_SIGN_COUNT


def space_click(event):
    """
    Event handler for the space key press event.
    This function is triggered when the space key is pressed. It performs the following actions:
    - Updates various global variables and counts the number of spaces pressed.
    - Compares the current word with the expected word from the WORDS_LIST.
    - Updates the letter counter, sign count, and text highlighting in the textbox.
    - Tracks mistakes made by the user.
    Parameters:
    event (Event): The space key press event object.
    Returns:
    None
    """
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
            MISTAKE_WORDS.append(WORDS_LIST[SPACE_COUNT - 1])
            USER_MISTAKES.append(CURRENT_WORD)
            start_idx = f"1.{ALL_SIGN_COUNT}"
            end_idx = f"1.{ALL_SIGN_COUNT + len(WORDS_LIST[SPACE_COUNT])}"
            textbox.tag_add("green_background", start_idx, end_idx)

    if text_entry.get() != "":
        text_entry.delete(0, tk.END)


def reset_call_count():
    """
    Resets the call count and sets the text color to white for the first character. This function resets the global
    variable tracking_function_call_count to 0 and sets the text color to white for the first character in the
    textbox.
    Parameters: None
    Returns: None
    """
    global tracking_function_call_count

    tracking_function_call_count = 0
    textbox.tag_configure("white_char", foreground='white')
    textbox.tag_add("white_char", '1.0')
    textbox.tag_raise("white_char")


def handle_backspace(char_position):
    """
    Handles the backspace key press by adjusting the call count and restoring the text color.
    This function is triggered when the backspace key is pressed. It performs the following actions:
    - Adjusts the call count and restores the text color for the previous character in the textbox.
    Parameters:
    char_position (int): The position of the character in the textbox.
    Returns:
    None
    """
    global tracking_function_call_count, ALL_SIGN_COUNT

    char_index = f"1.{char_position - 1}"
    space_index = textbox.index(f'1.{ALL_SIGN_COUNT - 1}')

    if char_index == space_index:
        return
    elif char_index == '1.-1':
        reset_call_count()
        return
    else:
        tracking_function_call_count -= 1
        char_position -= 1

    textbox.tag_configure("white_char", foreground='white')
    textbox.tag_add("white_char", char_index)
    textbox.tag_raise("white_char")


def track_typing_letters(event):
    """
    Main function to track typing progress, validate keys, and update text color in response to user input.
    Parameters:
    - event: the event object representing the key press event
    Returns:
    - None
    """
    global SPACE_COUNT, WORDS_LIST, tracking_function_call_count, USER_MISTAKES
    total_characters = sum(len(word) for word in WORDS_LIST) + len(WORDS_LIST) - 1
    char_left = total_characters - tracking_function_call_count
    actual_char_position = total_characters - char_left
    text_entry_word = text_entry.get()
    start_index = f"1.{actual_char_position}"
    counter = 0

    if SPACE_COUNT < len(WORDS_LIST):
        next_word = WORDS_LIST[SPACE_COUNT]
    else:
        next_word = ""

    if not is_valid_key(event):
        text_entry.insert(tk.END, text_entry.get())
        # Show a warning if an invalid key is pressed
        messagebox.showwarning("Invalid Key", "You can only use letters, space and BackSpace.")
        return

    if counter < len(text_entry_word) and text_entry_word[counter] == " ":
        counter += 1

    # Handle Backspace key press
    if event.keysym == 'BackSpace':
        if tracking_function_call_count == 1:
            handle_backspace(0)
        else:
            handle_backspace(actual_char_position)
        return

    # Handle Space key press
    if event.keysym == 'space':
        tracking_function_call_count = ALL_SIGN_COUNT - 1

    if len(text_entry_word) > len(next_word):
        tracking_function_call_count = ALL_SIGN_COUNT - 1 + len(next_word)
    for char in next_word:
        if counter < len(text_entry.get()):
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
    tracking_function_call_count += 1


def count_mistakes(correct_words, user_words):
    """
    Counts the mistakes made by the user in typing words.
    Args:
    - correct_words (list): List of correct words.
    - user_words (list): List of words typed by the user.
    Returns:
    - int: Number of mistakes made by the user.
    """
    mistake_count = 0
    for i in range(len(correct_words)):
        correct_word = correct_words[i]
        user_word = user_words[i] if i < len(user_words) else ""
        # Count differences in words
        min_length = min(len(correct_word), len(user_word))
        for j in range(len(user_word)):  # Iterating over the length of the user word
            if j < len(correct_word) and correct_word[j] != user_word[j]:
                mistake_count += 1
        # Counting additional mistakes if the user word is longer
        mistake_count += max(0, len(user_word) - len(correct_word))
    return mistake_count


def countdown_timer():
    """
    Function to implement a countdown timer for working seconds. It decrements the WORK_SEC variable,
    updates a meter, and schedules itself to run after 1 second until WORK_SEC reaches 0. When WORK_SEC reaches 0,
    it disables text entry, calculates points, and opens a secondary window.
    Parameters: - None
    Returns: - None
    """
    global WORK_SEC
    if WORK_SEC > 0:
        WORK_SEC -= 1
        meter.configure(amountused=0 + WORK_SEC)
        window.after(1000, countdown_timer)
    else:
        text_entry.config(state="disabled")
        count_points()
        open_secondary_window()


def on_first_letter(event):
    """
    Function called when the first letter is typed.
    It checks if the WORK_SEC is at its initial value and starts the countdown timer if it is.
    Parameters:
    - event: the event object representing the key press event
    Returns:
    - None
    """
    global WORK_SEC
    if WORK_SEC == 60:
        # Start the countdown timer only if it's not already running
        countdown_timer()


def count_points():
    """
    Function to calculate points based on the number of signs typed.
    It calculates the words per minute (wpm) based on the number of signs typed.
    Parameters:
    - None
    Returns:
    - raw_cmp, cmp, wpm
    """
    global ALL_SIGN_COUNT, LETTER_COUNTER
    raw_cpm = ALL_SIGN_COUNT
    cpm = LETTER_COUNTER
    wpm = round(cpm / 5)
    return raw_cpm, cpm, wpm


def open_secondary_window():
    """
    Function to open a secondary window after disabling text entry, focusing on the main window,
    calculating mistakes, creating a SecondaryWindow instance, resetting the program, and returning the secondary window.
    Parameters:
    - None
    Returns:
    - None
    """
    text_entry.config(state='disabled')
    window.focus()
    mistakes = count_mistakes(MISTAKE_WORDS, USER_MISTAKES)
    SecondaryWindow(ALL_SIGN_COUNT, LETTER_COUNTER, MISTAKE_WORDS, USER_MISTAKES, mistakes)
    reset_program()


def reset_program():
    """
    Function to reset the program variables and UI elements to their initial state.
    It resets various global variables, clears the textbox, inserts random words, sets tags for formatting,
    resets the text entry field, and configures the meter.
    Parameters:
    - None
    Returns:
    - None
    """
    global WORK_SEC, WORDS_LIST, CURRENT_WORD, SPACE_COUNT, LETTER_COUNTER, ALL_SIGN_COUNT, \
        tracking_function_call_count, MISTAKE_WORDS, USER_MISTAKES, start_idx, end_idx
    WORK_SEC = 60
    WORDS_LIST = []
    CURRENT_WORD = ''
    SPACE_COUNT = 0
    LETTER_COUNTER = 0
    ALL_SIGN_COUNT = 0
    tracking_function_call_count = 0
    MISTAKE_WORDS = []
    USER_MISTAKES = []

    textbox.delete('1.0', tk.END)
    textbox.tag_configure("white_char", foreground="white", spacing1=10, spacing2=10, justify='center',
                          font=("Helvetica", 30, 'bold'))
    textbox.insert(tk.END, random_words())
    start_idx = '1.0'
    end_idx = f'1.{len(WORDS_LIST[0])}'
    textbox.tag_add("green_background", start_idx, end_idx)
    textbox.tag_add("white_char", "1.0", tk.END)

    text_entry.delete(0, tk.END)
    text_entry.insert(0, "Type the words here.")
    text_entry.config(state="normal")
    meter.configure(amountused=60)


# ___________________________________________________________________________________________________
# -------------------------------------------- UI ---------------------------------------------------

window = ttk.Window()
window.title("Typing Speed Test")
window.config(padx=150, pady=200, bg=BEIGE)
custom_font = font.Font(family="Helvetica", size=40, weight="bold", underline=True, slant="roman")
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

textbox = tk.Text(window, width=120, height=13)
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
