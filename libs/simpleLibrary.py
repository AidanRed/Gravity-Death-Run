import os
import sys

#If the operating system is windows, then make the file path separator: \
if os.name.lower() == "nt":
    SEPARATOR = "\\"

#If the operating system is linux or osx, then make the file path separator: /
elif os.name.lower() == "posix":
    SEPARATOR = "/"


def clearScreen():
    if os.name.lower() == "nt":
        os.system("cls")

    elif os.name.lower() == "posix":
        os.system("clear")


def formatString(string1):
    """
    Removes whitespace from the front and back of the string, and makes it lower case.

    Parameters:

    string1: The string to format
    """
    return string1.lstrip().rstrip().lower()


def niceExit():
    """
    Wait for the user to press enter, then exit
    """
    raw_input("\nPress enter to exit...")
    sys.exit()


def forceFloat(message):
    """
    Force the user to enter a float.

    Parameters:

    message: The message used to request input
    """
    done = False
    while not done:
        input1 = raw_input(message)
        try:
            input1 = float(input1)
            done = True

        except ValueError:
            print "That was not a number!"

    return input1


def forceChoice(initialMessage, list1):
    """
    Force the user to enter valid input - the input must be in a list of valid inputs.

    Parameters:

    initialMessage: The message to request input

    list1: The list to test the input against
    """
    input1 = None

    while input1 not in list1:
        input1 = raw_input(initialMessage)

        if input1 not in list1:
            print "That is not a valid answer!\n"

    return input1

#Not the best system, but the more code the better.
def encrypt(number):
    return number/-3.6

def decrypt(number):
    return number*-3.6
