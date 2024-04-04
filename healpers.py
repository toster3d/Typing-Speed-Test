def is_valid_key(event):
    """
    Function to check if the pressed key is valid, including letters, space, backspace, or single quote.

    Parameters:
    - event: the key event to be checked

    Returns:
    - True if the pressed key is valid, False otherwise
    """
    return event.keysym in ['BackSpace', 'space'] or event.char.isalpha() or event.char == "'"