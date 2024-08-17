# Author: Brandon Mortimore
# Last Updated: 04/20/23
#
# Description: This file contains input validation functions.
# The functions take various types of inputs (int, float, etc)
# and validate that they're within the defined constraints
#
# Sources: 233Y code examples, PEP8 Standard Guide, Mod readings

def input_int(prompt="Please enter an integer: ", ge=None, gt=None, le=None, lt=None):
    """
    Function to ask for and return a valid integer
    :param prompt: string, Optional string for prompt
    :param ge: int, greater than or equal to constraint
    :param gt: int, greater than constraint
    :param le: int, less than or equal to constraint
    :param lt: int, less than constraint
    :return: int, a valid integer, optionally within a range
    """
    # Ask for int/check if within constraints/return num or re-loop
    while True:
        num = input(prompt)
        try:
            num = int(num)
            if (ge is None or num >= ge) and (gt is None or num > gt) \
                    and (le is None or num <= le) and (lt is None or num < lt):
                return num
            else:
                raise ValueError
        except:
            print("Error: Please enter a valid whole number within the specified range: ")


def input_float(prompt="Please enter a decimal number: ", ge=None, gt=None, le=None, lt=None):
    """
    Function to ask for and return a valid float value
    :param prompt: string, Optional string for prompt
    :param ge: float, greater than or equal to constraint
    :param gt: float, greater than constraint
    :param le: float, less than or equal to constraint
    :param lt: float, less than constraint
    :return: float, a valid float value/number, optionally within a range
    """
    # Ask for float/check if within constraints/return num or re-loop
    while True:
        num = input(prompt)
        try:
            num = float(num)
            if (ge is None or num >= ge) and (gt is None or num > gt) \
                    and (le is None or num <= le) and (lt is None or num < lt):
                return num
            else:
                raise ValueError
        except:
            print("Error: Please enter a valid decimal number within the specified range.")


def input_string(prompt="Please enter some text: ", valid=lambda x: x != ""):
    """
    Function to ask for and return a valid string of text
    :param prompt: string, Optional string for prompt
    :param valid: function, Optional validation function
    :return: string, a valid string of text/characters
    """
    text = ""

    # Ask for string/Check if valid/Return or re-loop
    while True:
        text = input(prompt)
        if valid(text):
            return text
        else:
            print("Error: Please enter a valid piece of text.")


def y_or_n(prompt="Please enter 'y' or 'n': "):
    """
    Function to return True for Yes variants False for No
    :param prompt: string, Optional string for prompt
    :return: bool, True for 'yes'/'y' and False for 'no'/'n'
    """
    # Init response/input prompt for Y/N
    response = ""
    response = input(prompt)
    response = response.lower()

    # Loop for Y/N response
    while response != "n" and response != "y" and response != "no" and response != "yes":
        print("Invalid response")
        response = input(prompt)
        response = response.lower()

    # Return True if Yes/False if No
    if response == "y" or response == "yes":
        return True
    else:
        return False


def select_item(prompt, choices, dictionary=None):
    """
    Function to ask and receive a choice from a list/dict
    :param prompt: string, Optional string for prompt
    :param choices: list, a list to select an item from
    :param dictionary: dict, an optional dictionary that maps possible inputs into outputs
    :return: the item that the user selected
    """
    # Iterate through list/Start index at 1/Print choices
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

    # Check for provided dict/Create dict
    if dictionary is None:
        dictionary = {}

    # Init bool flag as false
    valid_input = False
    while not valid_input:
        user_input = input(prompt).strip().lower()
        # Check for digit/decrement by 1 for 0 based index
        if user_input.isdigit():
            selected_index = int(user_input) - 1
            if 0 <= selected_index < len(choices):
                selected_item = choices[selected_index]
                valid_input = True
        # Check for key in dict/assign to selected_item
        elif user_input in dictionary:
            selected_item = dictionary[user_input]
            valid_input = True
        # Check for matching text input
        elif user_input in [choice.lower() for choice in choices]:
            selected_item = choices[[choice.lower() for choice in choices].index(user_input)]
            valid_input = True
        # Invalid input/restart loop
        if not valid_input:
            print("Invalid input. Please enter a valid option.")
    return selected_item


def input_value(value_type, prompt=None, ge=None, gt=None, le=None, lt=None,
                valid=None, choices=None, aliases=None):
    """
    Function that takes a type keyword and executes the associated
    function.
    :param value_type: string, value for type of function
    :param prompt: string, Optional string prompt
    :param ge: float, greater than or equal to constraint
    :param gt: float, greater than constraint
    :param le: float, less than or equal to constraint
    :param lt: float, less than constraint
    :param valid: function, Optional validation function
    :param choices: list, a list to select an item from
    :param aliases: dict, an optional dictionary that maps possible inputs into outputs
    :return: function, user specified input validation function
    """
    if value_type == "int":
        if prompt is None:
            prompt = "Please enter an integer: "
        return input_int(prompt, ge, gt, le, lt)
    elif value_type == "float":
        if prompt is None:
            prompt = "Please enter a decimal number: "
        return input_float(prompt, ge, gt, le, lt)
    elif value_type == "string":
        if prompt is None:
            prompt = "Please enter some text: "
        if valid is None:
            valid = lambda x: x != ""
        return input_string(prompt, valid)
    elif value_type == "y_or_n":
        if prompt is None:
            prompt = "Please enter 'y' or 'n': "
        return y_or_n(prompt)
    elif value_type == "select_item":
        if prompt is None:
            prompt = "Select an option: "
        if choices is None:
            raise ValueError("Choices must be provided for type 'select_item'")
        return select_item(prompt, choices, aliases)
    else:
        raise ValueError("Invalid type specified")

